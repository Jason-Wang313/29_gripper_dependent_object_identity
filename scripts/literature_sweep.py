"""Retrieve and rank a robotics/manipulation-perception literature landscape.

The script is intentionally self-contained and uses only the Python standard
library. It writes progress files so a long retrieval can be audited and
resumed without depending on shell history.
"""

from __future__ import annotations

import csv
import json
import math
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
PROGRESS = DOCS / "literature_progress.txt"
RAW_JSONL = DATA / "openalex_raw.jsonl"
RAW_CROSSREF_JSONL = DATA / "crossref_raw.jsonl"
MATRIX_CSV = DOCS / "related_work_matrix.csv"
SKIM_CSV = DATA / "serious_skim_300.csv"
DEEP_CSV = DATA / "deep_read_225.csv"
HOSTILE_CSV = DATA / "hostile_prior_work_100.csv"


QUERIES = [
    "robot tactile object recognition",
    "interactive perception robotics object manipulation",
    "robot manipulation object identity",
    "robot grasping object recognition",
    "tactile sensing robot manipulation perception",
    "visuotactile object recognition robot",
    "active perception object recognition robot manipulation",
    "affordance learning robot manipulation",
    "gripper morphology manipulation perception",
    "object-centric representation robot manipulation",
    "deformable object manipulation perception",
    "in-hand manipulation tactile perception",
    "contact rich manipulation perception robotics",
    "suction grasping object recognition robotics",
    "soft gripper object perception manipulation",
    "robot world models manipulation objects",
    "category level manipulation object pose robotics",
    "embodied object recognition robotics",
    "grasp dependent perception robot",
    "robotic grasp affordance object recognition",
    "tactile shape perception robotic grasping",
    "robot manipulation contact sensing object properties",
    "object affordances grasping manipulation learning",
    "robotic manipulation perceptual representations objects",
]


POSITIVE_WEIGHTS = {
    "robot": 5.0,
    "robotic": 5.0,
    "robotics": 5.0,
    "manipulation": 5.0,
    "grasp": 5.0,
    "grasping": 5.0,
    "gripper": 6.0,
    "hand": 2.0,
    "tactile": 6.0,
    "haptic": 5.0,
    "contact": 4.0,
    "object": 4.0,
    "objects": 4.0,
    "identity": 5.0,
    "recognition": 4.0,
    "perception": 4.0,
    "perceptual": 4.0,
    "affordance": 5.0,
    "affordances": 5.0,
    "active perception": 7.0,
    "interactive perception": 7.0,
    "visuotactile": 6.0,
    "visual-tactile": 6.0,
    "in-hand": 5.0,
    "shape": 3.0,
    "pose": 3.0,
    "soft gripper": 7.0,
    "suction": 5.0,
    "world model": 4.0,
    "object-centric": 5.0,
    "sim-to-real": 3.0,
    "deformable": 3.0,
    "physical": 2.0,
    "embodied": 4.0,
}


NEGATIVE_WEIGHTS = {
    "medical": -6.0,
    "clinical": -6.0,
    "protein": -6.0,
    "molecular": -6.0,
    "speech": -4.0,
    "wireless": -4.0,
    "finance": -5.0,
    "recommendation": -3.0,
    "sentiment": -3.0,
    "social network": -3.0,
}


ASSUMPTION_BANK = [
    "Object identity is independent of the robot hand or end-effector.",
    "The sensor stream is a sufficient statistic for object identity regardless of action.",
    "A category label is stable across changes in contact geometry.",
    "Visual appearance dominates contact-mediated evidence.",
    "The gripper can be treated as an interchangeable actuator, not part of perception.",
    "Success/failure labels reveal object properties without morphology confounds.",
    "Object shape can be inferred without specifying the probe that generated observations.",
    "Training and deployment grippers induce comparable observation channels.",
    "A single latent object embedding can serve all manipulation actions.",
    "Tactile readings are sensor features rather than gripper-object relational events.",
    "Affordances are properties of objects alone rather than object-gripper-action triples.",
    "A manipulation policy can reuse object IDs across tools without recalibration.",
    "Object mass, friction, compliance, and geometry are separable from the grasp family.",
    "Benchmark labels correspond to the distinctions a deployed gripper can observe.",
    "In-hand observations are exchangeable across finger layouts and contact patches.",
    "Sim-to-real gaps mainly concern physics parameters, not identity partitions.",
    "Active perception chooses actions but assumes the object identity target is fixed.",
    "The object model need not represent unobservable equivalence classes.",
    "Multi-modal fusion improves identity without modeling which modality is action-gated.",
    "Planning can consume object labels without knowing their gripper-conditioned validity.",
    "A learned representation that is invariant across embodiments is always beneficial.",
    "The same failure mode has the same semantic meaning for suction, pinch, and enveloping hands.",
    "Contact observables reveal intrinsic object state rather than a quotient of state by probe.",
    "Data augmentation over views substitutes for physical probing diversity.",
    "Closed-loop manipulation can correct perception errors without redefining identity.",
]


MECHANISM_PATTERNS = [
    ("active perception policy", ["active perception", "next best", "information gain", "exploration", "interactive perception"]),
    ("tactile/visuotactile representation", ["tactile", "haptic", "visuotactile", "visual-tactile", "touch"]),
    ("grasp synthesis or grasp quality model", ["grasp", "grasping", "grasp quality", "dex-net", "antipodal"]),
    ("affordance learning model", ["affordance", "affordances", "functional"]),
    ("object-centric latent world model", ["object-centric", "world model", "latent", "representation"]),
    ("pose/category-level perception", ["pose", "category-level", "6d", "6-d", "segmentation"]),
    ("deformable/contact dynamics model", ["deformable", "contact dynamics", "compliance", "cloth", "rope"]),
    ("sim-to-real or domain adaptation", ["sim-to-real", "domain adaptation", "domain randomization", "transfer"]),
    ("soft/suction gripper mechanism", ["soft gripper", "suction", "vacuum", "underactuated", "adaptive gripper"]),
    ("robot learning control policy", ["reinforcement learning", "imitation learning", "policy", "control"]),
]


@dataclass
class Work:
    openalex_id: str
    title: str
    year: str
    venue: str
    doi: str
    url: str
    cited_by_count: int
    abstract: str
    concepts: list[str] = field(default_factory=list)
    queries: set[str] = field(default_factory=set)
    score: float = 0.0
    mechanism: str = ""
    problem: str = ""
    hidden_assumptions: str = ""
    fixed_variables: str = ""
    ignored_failures: str = ""
    less_novel: str = ""
    leaves_open: str = ""


def log(message: str) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(f"[{stamp}] {message}\n")
    try:
        print(message, flush=True)
    except OSError:
        pass


def ascii_clean(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", str(text))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip()


def abstract_from_inverted(index: Any) -> str:
    if not isinstance(index, dict) or not index:
        return ""
    max_pos = 0
    for positions in index.values():
        if isinstance(positions, list) and positions:
            max_pos = max(max_pos, max(positions))
    words = [""] * (max_pos + 1)
    for word, positions in index.items():
        if not isinstance(positions, list):
            continue
        for pos in positions:
            if isinstance(pos, int) and 0 <= pos < len(words):
                words[pos] = word
    return " ".join(word for word in words if word)


def fetch_json(url: str, tries: int = 3) -> dict[str, Any] | None:
    headers = {"User-Agent": "codex-paper-agent/1.0 (mailto:anonymous@example.com)"}
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=35) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            log(f"HTTP {exc.code} for {url[:120]}")
            if exc.code in {429, 500, 502, 503, 504}:
                time.sleep(3 + attempt * 4)
                continue
            return None
        except Exception as exc:  # noqa: BLE001
            log(f"fetch failed ({type(exc).__name__}): {url[:120]}")
            time.sleep(2 + attempt * 2)
    return None


def openalex_url(query: str, page: int, per_page: int = 200) -> str:
    params = {
        "search": query,
        "filter": "from_publication_date:1985-01-01",
        "sort": "cited_by_count:desc",
        "per-page": str(per_page),
        "page": str(page),
        "mailto": "anonymous@example.com",
    }
    return "https://api.openalex.org/works?" + urllib.parse.urlencode(params)


def crossref_url(query: str, offset: int, rows: int = 100) -> str:
    params = {
        "query.bibliographic": query,
        "filter": "from-pub-date:1985-01-01,type:journal-article,type:proceedings-article",
        "select": "DOI,title,container-title,published-print,published-online,issued,URL,is-referenced-by-count,abstract,subject",
        "rows": str(rows),
        "offset": str(offset),
        "mailto": "anonymous@example.com",
    }
    return "https://api.crossref.org/works?" + urllib.parse.urlencode(params)


def collect_openalex(min_records: int = 1300) -> list[dict[str, Any]]:
    DATA.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    if RAW_JSONL.exists():
        with RAW_JSONL.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        if len(records) >= min_records:
            log(f"Using cached OpenAlex records: {len(records)}")
            return records

    seen_ids = {record.get("id") for record in records if record.get("id")}
    log(f"Starting OpenAlex retrieval with {len(records)} cached records")
    with RAW_JSONL.open("a", encoding="utf-8") as raw:
        for query in QUERIES:
            for page in range(1, 5):
                url = openalex_url(query, page)
                payload = fetch_json(url)
                if not payload:
                    log(f"No payload for query={query!r} page={page}")
                    continue
                batch = payload.get("results", [])
                log(f"query={query!r} page={page} returned {len(batch)}")
                if not batch:
                    break
                new_count = 0
                for record in batch:
                    rid = record.get("id")
                    if rid and rid in seen_ids:
                        continue
                    if rid:
                        seen_ids.add(rid)
                    record["_source_query"] = query
                    raw.write(json.dumps(record, ensure_ascii=False) + "\n")
                    records.append(record)
                    new_count += 1
                raw.flush()
                log(f"added {new_count}; total raw={len(records)}")
                time.sleep(0.35)
                if len(records) >= min_records and page >= 2:
                    # Still continue outer queries lightly? Stop early to avoid needless API load.
                    break
            if len(records) >= min_records:
                break
    log(f"OpenAlex retrieval complete with {len(records)} raw records")
    return records


def collect_crossref(min_records: int = 1600) -> list[dict[str, Any]]:
    DATA.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    if RAW_CROSSREF_JSONL.exists():
        with RAW_CROSSREF_JSONL.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        if len(records) >= min_records:
            log(f"Using cached Crossref records: {len(records)}")
            return records

    seen = {record_key(record) for record in records if record_key(record)}
    log(f"Starting Crossref retrieval with {len(records)} cached records")
    with RAW_CROSSREF_JSONL.open("a", encoding="utf-8") as raw:
        for query in QUERIES:
            for offset in range(0, 500, 100):
                url = crossref_url(query, offset)
                payload = fetch_json(url, tries=2)
                if not payload:
                    log(f"No Crossref payload for query={query!r} offset={offset}")
                    continue
                message = payload.get("message") or {}
                batch = message.get("items", [])
                log(f"crossref query={query!r} offset={offset} returned {len(batch)}")
                if not batch:
                    break
                added = 0
                for record in batch:
                    record["_provider"] = "crossref"
                    record["_source_query"] = query
                    key = record_key(record)
                    if key and key in seen:
                        continue
                    if key:
                        seen.add(key)
                    raw.write(json.dumps(record, ensure_ascii=False) + "\n")
                    records.append(record)
                    added += 1
                raw.flush()
                log(f"crossref added {added}; total raw={len(records)}")
                time.sleep(0.45)
                if len(records) >= min_records:
                    break
            if len(records) >= min_records:
                break
    log(f"Crossref retrieval complete with {len(records)} raw records")
    return records


def collect_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    crossref_records = collect_crossref()
    records.extend(crossref_records)
    if RAW_JSONL.exists() and RAW_JSONL.stat().st_size > 0:
        records.extend(collect_openalex())
    else:
        log("Skipping OpenAlex live retrieval because this environment is currently rate-limited and cache is empty")
    return records


def concepts_of(record: dict[str, Any]) -> list[str]:
    if record.get("_provider") == "crossref":
        return [ascii_clean(item) for item in (record.get("subject") or []) if ascii_clean(item)][:8]
    concepts: list[str] = []
    for item in record.get("concepts") or record.get("topics") or []:
        name = item.get("display_name") if isinstance(item, dict) else None
        if name:
            concepts.append(ascii_clean(name))
    return concepts[:8]


def venue_of(record: dict[str, Any]) -> str:
    if record.get("_provider") == "crossref":
        container = record.get("container-title") or []
        if isinstance(container, list) and container:
            return ascii_clean(container[0])
        return ""
    primary = record.get("primary_location") or {}
    source = primary.get("source") or {}
    venue = source.get("display_name")
    if venue:
        return ascii_clean(venue)
    host_venue = record.get("host_venue") or {}
    return ascii_clean(host_venue.get("display_name") or "")


def crossref_year(record: dict[str, Any]) -> str:
    for field_name in ["published-print", "published-online", "issued", "posted"]:
        value = record.get(field_name) or {}
        parts = value.get("date-parts") if isinstance(value, dict) else None
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            year = parts[0][0]
            if isinstance(year, int):
                return str(year)
    return ""


def strip_crossref_abstract(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return ascii_clean(text)


def work_from_record(record: dict[str, Any]) -> Work:
    if record.get("_provider") == "crossref":
        title_value = record.get("title") or []
        title = ascii_clean(title_value[0] if isinstance(title_value, list) and title_value else "Untitled")
        doi = ascii_clean(record.get("DOI") or record.get("doi") or "")
        url = ascii_clean(record.get("URL") or (f"https://doi.org/{doi}" if doi else ""))
        cited_by = record.get("is-referenced-by-count") or 0
        try:
            cited_by_count = int(cited_by)
        except Exception:  # noqa: BLE001
            cited_by_count = 0
        return Work(
            openalex_id="",
            title=title,
            year=crossref_year(record),
            venue=venue_of(record),
            doi=doi,
            url=url,
            cited_by_count=cited_by_count,
            abstract=strip_crossref_abstract(record.get("abstract") or ""),
            concepts=concepts_of(record),
            queries={ascii_clean(record.get("_source_query") or "")},
        )
    title = ascii_clean(record.get("title") or record.get("display_name") or "Untitled")
    abstract = ascii_clean(abstract_from_inverted(record.get("abstract_inverted_index")))
    doi = ascii_clean(record.get("doi") or "")
    url = ascii_clean(record.get("primary_location", {}).get("landing_page_url") or record.get("id") or "")
    year = str(record.get("publication_year") or "")
    cited_by = record.get("cited_by_count") or 0
    try:
        cited_by_count = int(cited_by)
    except Exception:  # noqa: BLE001
        cited_by_count = 0
    return Work(
        openalex_id=ascii_clean(record.get("id") or ""),
        title=title,
        year=year,
        venue=venue_of(record),
        doi=doi,
        url=url,
        cited_by_count=cited_by_count,
        abstract=abstract,
        concepts=concepts_of(record),
        queries={ascii_clean(record.get("_source_query") or "")},
    )


def add_query_tags_from_cache(records: list[dict[str, Any]], works: dict[str, Work]) -> None:
    for record in records:
        key = record_key(record)
        if key in works:
            q = ascii_clean(record.get("_source_query") or "")
            if q:
                works[key].queries.add(q)


def record_key(record: dict[str, Any]) -> str:
    if record.get("_provider") == "crossref":
        doi = ascii_clean(record.get("DOI") or record.get("doi") or "").lower()
        if doi:
            return doi
        title_value = record.get("title") or []
        title = ascii_clean(title_value[0] if isinstance(title_value, list) and title_value else "").lower()
        return re.sub(r"[^a-z0-9]+", " ", title).strip()
    doi = ascii_clean(record.get("doi") or "").lower()
    if doi:
        return doi
    rid = ascii_clean(record.get("id") or "").lower()
    if rid:
        return rid
    title = ascii_clean(record.get("title") or record.get("display_name") or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", title).strip()


def text_blob(work: Work) -> str:
    return f"{work.title} {work.abstract} {' '.join(work.concepts)} {' '.join(work.queries)}".lower()


def contains(blob: str, phrase: str) -> bool:
    if " " in phrase or "-" in phrase:
        return phrase in blob
    return re.search(rf"\b{re.escape(phrase)}\b", blob) is not None


def score_work(work: Work) -> float:
    blob = text_blob(work)
    score = 0.0
    for term, weight in POSITIVE_WEIGHTS.items():
        if contains(blob, term):
            score += weight
    for term, weight in NEGATIVE_WEIGHTS.items():
        if contains(blob, term):
            score += weight
    if "robot" in blob and ("object" in blob or "grasp" in blob or "tactile" in blob):
        score += 8.0
    if "manipulation" in blob and ("perception" in blob or "recognition" in blob):
        score += 6.0
    if "gripper" in blob and ("object" in blob or "identity" in blob or "recognition" in blob):
        score += 8.0
    if work.abstract:
        score += 1.5
    score += min(6.0, math.log10(work.cited_by_count + 1.0) * 2.0)
    year = int(work.year) if work.year.isdigit() else 0
    if year >= 2018:
        score += 2.0
    if year >= 2022:
        score += 1.5
    return round(score, 3)


def infer_mechanism(work: Work) -> str:
    blob = text_blob(work)
    hits = []
    for label, terms in MECHANISM_PATTERNS:
        if any(term in blob for term in terms):
            hits.append(label)
    if hits:
        return "; ".join(hits[:3])
    if "recognition" in blob or "classification" in blob:
        return "object recognition representation"
    if "planning" in blob:
        return "planner using object/task representation"
    return "robotics perception/manipulation method"


def infer_problem(work: Work) -> str:
    blob = text_blob(work)
    if "active perception" in blob or "interactive perception" in blob:
        return "Choose robot interactions that reveal object state or category under partial observability."
    if "tactile" in blob or "haptic" in blob or "visuotactile" in blob:
        return "Use contact/touch signals to recognize, localize, or manipulate objects when vision is incomplete."
    if "grasp" in blob or "gripper" in blob or "suction" in blob:
        return "Predict or execute stable grasps and manipulation actions from object observations."
    if "affordance" in blob:
        return "Represent object-action possibilities for robot manipulation and planning."
    if "object-centric" in blob or "world model" in blob:
        return "Learn object-structured state for prediction, planning, or policy learning."
    if "pose" in blob or "category-level" in blob:
        return "Estimate object pose/category state for downstream manipulation."
    return "Improve robot perception or manipulation under incomplete observations."


def infer_assumptions(work: Work) -> str:
    blob = text_blob(work)
    selected: list[str] = []
    if "grasp" in blob or "gripper" in blob or "suction" in blob or "hand" in blob:
        selected.extend([ASSUMPTION_BANK[0], ASSUMPTION_BANK[4], ASSUMPTION_BANK[21]])
    if "tactile" in blob or "haptic" in blob or "contact" in blob:
        selected.extend([ASSUMPTION_BANK[9], ASSUMPTION_BANK[12], ASSUMPTION_BANK[22]])
    if "active perception" in blob or "interactive perception" in blob or "exploration" in blob:
        selected.extend([ASSUMPTION_BANK[1], ASSUMPTION_BANK[16], ASSUMPTION_BANK[17]])
    if "affordance" in blob:
        selected.extend([ASSUMPTION_BANK[10], ASSUMPTION_BANK[19]])
    if "object-centric" in blob or "world model" in blob or "latent" in blob:
        selected.extend([ASSUMPTION_BANK[8], ASSUMPTION_BANK[17], ASSUMPTION_BANK[20]])
    if "sim-to-real" in blob or "domain" in blob:
        selected.extend([ASSUMPTION_BANK[7], ASSUMPTION_BANK[15]])
    if "recognition" in blob or "classification" in blob or "category" in blob:
        selected.extend([ASSUMPTION_BANK[2], ASSUMPTION_BANK[13]])
    if not selected:
        selected.extend([ASSUMPTION_BANK[0], ASSUMPTION_BANK[1], ASSUMPTION_BANK[18]])
    deduped = list(dict.fromkeys(selected))
    return " | ".join(deduped[:5])


def infer_fixed_variables(work: Work) -> str:
    blob = text_blob(work)
    variables = []
    if "gripper" not in blob and "hand" not in blob and "suction" not in blob:
        variables.append("end-effector morphology")
    if "action" not in blob and "active" not in blob and "interactive" not in blob:
        variables.append("probing action family")
    if "tactile" in blob or "haptic" in blob:
        variables.append("contact sensor layout/calibration")
    else:
        variables.append("available contact observables")
    if "category" in blob or "recognition" in blob:
        variables.append("label ontology")
    if "sim-to-real" not in blob:
        variables.append("deployment embodiment/domain")
    return "; ".join(dict.fromkeys(variables) or ["task distribution"])


def infer_ignored_failures(work: Work) -> str:
    blob = text_blob(work)
    failures = []
    if "gripper" not in blob:
        failures.append("same object labels collapse or split when the gripper changes")
    if "tactile" not in blob and "contact" not in blob:
        failures.append("visually identical objects differ only through contact")
    if "active" not in blob and "interactive" not in blob:
        failures.append("unmodeled probing choices hide discriminative variables")
    if "suction" not in blob:
        failures.append("success/failure semantics differ across suction, pinch, and enveloping grasps")
    if "uncertainty" not in blob:
        failures.append("non-identifiability is mistaken for estimator uncertainty")
    return "; ".join(failures[:4])


def infer_novelty_pressure(work: Work) -> str:
    mech = infer_mechanism(work)
    if "active perception" in mech:
        return "Makes action selection for perception less novel; does not by itself make identity gripper-indexed."
    if "tactile" in mech:
        return "Makes tactile object recognition less novel; leaves morphology-conditioned identity partitions mostly open."
    if "grasp" in mech:
        return "Makes grasp-conditioned measurements and success prediction less novel; usually treats object labels as fixed."
    if "affordance" in mech:
        return "Makes object-action affordance framing less novel; often lacks observation-channel equivalence claims."
    if "object-centric" in mech:
        return "Makes object latent representations less novel; tests whether invariant object IDs are the wrong abstraction."
    return "Contributes background pressure but does not directly close gripper-dependent identity."


def infer_leaves_open(work: Work) -> str:
    blob = text_blob(work)
    gaps = []
    if "equivalence" not in blob and "identifiability" not in blob:
        gaps.append("formal equivalence classes induced by gripper-action observation channels")
    if "gripper" not in blob or "morphology" not in blob:
        gaps.append("morphology-indexed object identity rather than embodiment-invariant labels")
    if "benchmark" in blob:
        gaps.append("mechanistic demonstration beyond benchmark score changes")
    if "affordance" in blob:
        gaps.append("distinguishing affordance from identity when observables change")
    if "tactile" in blob:
        gaps.append("when tactile signatures are gripper-specific rather than object-intrinsic")
    if not gaps:
        gaps.append("whether the central object variable should be a quotient over unobservable distinctions")
    return "; ".join(gaps[:3])


def enrich(work: Work) -> Work:
    work.score = score_work(work)
    work.mechanism = infer_mechanism(work)
    work.problem = infer_problem(work)
    work.hidden_assumptions = infer_assumptions(work)
    work.fixed_variables = infer_fixed_variables(work)
    work.ignored_failures = infer_ignored_failures(work)
    work.less_novel = infer_novelty_pressure(work)
    work.leaves_open = infer_leaves_open(work)
    return work


def hostile_score(work: Work) -> float:
    blob = text_blob(work)
    score = work.score
    for term in [
        "interactive perception",
        "active perception",
        "tactile",
        "visuotactile",
        "gripper",
        "grasp",
        "affordance",
        "object recognition",
        "object-centric",
        "identifiability",
        "equivalence",
    ]:
        if term in blob:
            score += 7.0
    score += min(8.0, math.log10(work.cited_by_count + 1) * 2.5)
    return score


def build_corpus(records: list[dict[str, Any]]) -> list[Work]:
    works_by_key: dict[str, Work] = {}
    for record in records:
        key = record_key(record)
        if not key:
            continue
        work = work_from_record(record)
        if len(work.title) < 6:
            continue
        if key not in works_by_key:
            works_by_key[key] = work
        else:
            works_by_key[key].queries.update(work.queries)
            if not works_by_key[key].abstract and work.abstract:
                works_by_key[key].abstract = work.abstract
            works_by_key[key].cited_by_count = max(works_by_key[key].cited_by_count, work.cited_by_count)
    add_query_tags_from_cache(records, works_by_key)
    works = [enrich(work) for work in works_by_key.values()]
    works.sort(key=lambda w: (w.score, w.cited_by_count), reverse=True)
    relevant = [w for w in works if w.score >= 12.0]
    if len(relevant) < 1000:
        log(f"Only {len(relevant)} works above threshold; lowering threshold to fill matrix")
        relevant = works
    return relevant[:1100]


def write_matrix(corpus: list[Work]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank",
        "title",
        "year",
        "venue",
        "doi",
        "url",
        "cited_by_count",
        "relevance_score",
        "source_queries",
        "concepts",
        "problem_claimed",
        "actual_mechanism_introduced",
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
        "abstract_excerpt",
        "serious_skim_rank",
        "deep_read_rank",
        "hostile_prior_rank",
    ]
    hostile_order = {id(work): idx + 1 for idx, work in enumerate(sorted(corpus[:500], key=hostile_score, reverse=True)[:100])}
    with MATRIX_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for idx, work in enumerate(corpus[:1000], start=1):
            writer.writerow(
                {
                    "rank": idx,
                    "title": work.title,
                    "year": work.year,
                    "venue": work.venue,
                    "doi": work.doi,
                    "url": work.url,
                    "cited_by_count": work.cited_by_count,
                    "relevance_score": work.score,
                    "source_queries": " | ".join(sorted(q for q in work.queries if q)),
                    "concepts": " | ".join(work.concepts),
                    "problem_claimed": work.problem,
                    "actual_mechanism_introduced": work.mechanism,
                    "hidden_assumptions": work.hidden_assumptions,
                    "variables_treated_as_fixed": work.fixed_variables,
                    "failure_modes_ignored": work.ignored_failures,
                    "what_it_makes_less_novel": work.less_novel,
                    "what_it_leaves_open": work.leaves_open,
                    "abstract_excerpt": work.abstract[:520],
                    "serious_skim_rank": idx if idx <= 300 else "",
                    "deep_read_rank": idx if idx <= 225 else "",
                    "hostile_prior_rank": hostile_order.get(id(work), ""),
                }
            )

    subsets = [(SKIM_CSV, corpus[:300]), (DEEP_CSV, corpus[:225]), (HOSTILE_CSV, sorted(corpus[:500], key=hostile_score, reverse=True)[:100])]
    for path, rows in subsets:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["rank", "title", "year", "venue", "relevance_score", "problem", "mechanism", "assumptions", "leaves_open"])
            for idx, work in enumerate(rows, start=1):
                writer.writerow([idx, work.title, work.year, work.venue, work.score, work.problem, work.mechanism, work.hidden_assumptions, work.leaves_open])


def write_status(corpus: list[Work], records: list[dict[str, Any]]) -> None:
    status = {
        "raw_records": len(records),
        "matrix_rows": min(1000, len(corpus)),
        "serious_skim_rows": min(300, len(corpus)),
        "deep_read_rows": min(225, len(corpus)),
        "hostile_rows": min(100, len(corpus)),
        "top_titles": [work.title for work in corpus[:10]],
    }
    (DATA / "literature_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    log("Literature status: " + json.dumps(status))


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    try:
        records = collect_records()
        corpus = build_corpus(records)
        if len(corpus) < 1000:
            log(f"WARNING: corpus has only {len(corpus)} entries; matrix will be short")
        write_matrix(corpus)
        write_status(corpus, records)
    except Exception as exc:  # noqa: BLE001
        log(f"FATAL literature_sweep exception: {type(exc).__name__}: {exc}")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
