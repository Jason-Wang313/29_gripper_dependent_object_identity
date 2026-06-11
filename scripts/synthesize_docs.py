"""Generate literature and novelty documents from the related-work matrix."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
MATRIX = DOCS / "related_work_matrix.csv"


HIDDEN_ASSUMPTIONS = [
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


def read_rows() -> list[dict[str, str]]:
    with MATRIX.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def short(text: str, n: int = 110) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 3] + "..."


def mechanism_counts(rows: list[dict[str, str]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for part in row["actual_mechanism_introduced"].split(";"):
            label = part.strip()
            if label:
                counts[label] += 1
    return counts


def year_bins(rows: list[dict[str, str]]) -> Counter[str]:
    bins: Counter[str] = Counter()
    for row in rows:
        year = row.get("year", "")
        if not year.isdigit():
            bins["unknown"] += 1
            continue
        y = int(year)
        if y < 2000:
            bins["pre-2000"] += 1
        elif y < 2010:
            bins["2000-2009"] += 1
        elif y < 2020:
            bins["2010-2019"] += 1
        else:
            bins["2020-2026"] += 1
    return bins


def hostile_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    hostile = [r for r in rows if r.get("hostile_prior_rank")]
    hostile.sort(key=lambda r: int(r["hostile_prior_rank"]))
    return hostile[:100]


def top_titles(rows: list[dict[str, str]], n: int = 12) -> str:
    lines = []
    for row in rows[:n]:
        lines.append(
            f"- {row['rank']}. {row['title']} ({row.get('year') or 'n.d.'}, "
            f"{row.get('venue') or 'venue unknown'}): {short(row['what_it_leaves_open'], 150)}"
        )
    return "\n".join(lines)


def write_literature_map(rows: list[dict[str, str]]) -> None:
    mechanisms = mechanism_counts(rows)
    years = year_bins(rows)
    hostile = hostile_rows(rows)
    content = f"""# Literature Map

## Corpus
- Landscape sweep: {len(rows)} rows in `docs/related_work_matrix.csv`.
- Serious skim: 300 highest-scored rows in `data/serious_skim_300.csv`.
- Deep read: 225 highest-scored rows in `data/deep_read_225.csv`.
- Hostile set: 100 closest rows in `data/hostile_prior_work_100.csv` and expanded in `docs/hostile_prior_work.md`.
- Retrieval source: Crossref metadata/abstracts because OpenAlex and Semantic Scholar returned HTTP 429 during this attempt. This is enough for a broad map, but it is not a substitute for a final human full-PDF literature review.

## Field Box
The relevant field box is manipulation perception for embodied agents: tactile and visuotactile object recognition, active/interactive perception, gripper hardware that changes sensing, object-centric manipulation representations, affordance learning, and task-conditioned manipulation planning.

The strongest boundary question is not whether touch improves object recognition. The stronger question is whether "object identity" itself should be indexed by the robot interface when the gripper-action channel changes what can be observed and what distinctions matter for control.

## Time Distribution
{json.dumps(dict(years), indent=2)}

## Mechanism Clusters
{json.dumps(dict(mechanisms.most_common()), indent=2)}

## High-Pressure Papers
{top_titles(rows, 20)}

## Hostile Center of Mass
{top_titles(hostile, 20)}

## Hidden Assumptions That May Be False
""" + "\n".join(f"{idx}. {item}" for idx, item in enumerate(HIDDEN_ASSUMPTIONS, 1)) + """

## Directions Considered
1. Bigger tactile recognition model: rejected because it keeps the object label fixed and only improves estimation.
2. Active probing for object classification: rejected as central contribution because active perception already chooses actions under a fixed target identity.
3. Multi-gripper benchmark: rejected as central contribution because a benchmark alone does not change the mechanism.
4. Affordance-only reframing: useful but insufficient because affordances can still assume object labels are stable and separate from the observing interface.
5. Interface-conditioned identity partitions: chosen because it changes the central variable from an embodiment-invariant object ID to the quotient of latent object states induced by a gripper-action observation channel.

## Chosen Direction
The paper should formalize and test interface-conditioned identity partitions. The core move is to treat each gripper-action family as inducing an observation-and-control equivalence relation over latent object states. A "same object" relation for manipulation is then not universal; it is indexed by the interface that produces the observables.
"""
    (DOCS / "literature_map.md").write_text(content, encoding="utf-8")


def write_hostile(rows: list[dict[str, str]]) -> None:
    hostile = hostile_rows(rows)
    lines = [
        "# Hostile Prior Work",
        "",
        "The hostile set is the 100 closest papers under the ranking heuristic, emphasizing active/interactive perception, tactile or visuotactile recognition, gripper-specific hardware, grasping, affordances, and object-centric manipulation. Each row states what the prior paper makes less novel and what remains open for interface-conditioned identity.",
        "",
        "| # | Paper | Problem | Mechanism | Hidden assumptions | Fixed variables | Ignored failures | Less novel | Leaves open |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in hostile:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["hostile_prior_rank"],
                    md_escape(short(f"{row['title']} ({row.get('year') or 'n.d.'})", 90)),
                    md_escape(short(row["problem_claimed"], 95)),
                    md_escape(short(row["actual_mechanism_introduced"], 95)),
                    md_escape(short(row["hidden_assumptions"], 120)),
                    md_escape(short(row["variables_treated_as_fixed"], 90)),
                    md_escape(short(row["failure_modes_ignored"], 120)),
                    md_escape(short(row["what_it_makes_less_novel"], 120)),
                    md_escape(short(row["what_it_leaves_open"], 120)),
                ]
            )
            + " |"
        )
    (DOCS / "hostile_prior_work.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_novelty_boundary() -> None:
    content = """# Novelty Boundary Map

## What Prior Work Already Covers
- Tactile and visuotactile recognition: recognizing objects or properties from contact streams is well covered.
- Active and interactive perception: choosing actions to reveal state under partial observability is well covered.
- Grasp success prediction and gripper design: gripper morphology, suction, soft grippers, and in-hand mechanisms are well covered.
- Affordance learning: object-action possibility representations are well covered.
- Object-centric latent world models: learned object representations for planning are well covered.

## What The Chosen Paper Must Not Claim
- It must not claim the first tactile object recognition method.
- It must not claim the first active perception method.
- It must not claim gripper morphology has never mattered.
- It must not claim a new benchmark is itself the contribution.
- It must not claim that uncertainty, active learning, or a verifier solves the problem.

## Boundary Where Novelty Remains
The unclaimed boundary is a representational one: define identity as an interface-conditioned quotient of latent object states, then prove that non-nested gripper-induced partitions make a single embodiment-invariant identity either unobservable for some gripper or insufficient for some manipulation outcome.

## Closest Hostile Families
1. Interactive perception papers: close because they make action part of perception, but they typically keep the target object variable fixed.
2. Tactile object recognition papers: close because they use touch to classify, but the classes are treated as object-intrinsic.
3. Gripper hardware/perception papers: close because they expose morphology-specific observables, but they usually optimize the sensor or controller rather than redefining identity.
4. Affordance papers: close because they bind action and object, but they often model action possibilities rather than observation-channel equivalence classes.
5. Object-centric manipulation/world-model papers: close because they learn object variables, but they usually prefer invariance across embodiments.
"""
    (DOCS / "novelty_boundary_map.md").write_text(content, encoding="utf-8")


def write_decision() -> None:
    content = """# Novelty Decision

## Decision
Proceed with the thesis: **object identity for robot manipulation should be represented as an interface-conditioned partition, not as a single gripper-agnostic label, whenever different gripper-action channels induce non-nested observability relations.**

## New Central Mechanism
The central mechanism is the **Interface-Conditioned Identity Partition (ICIP)**. For a gripper-action family `g`, ICIP defines two latent object states as the same identity when their observation distributions and task-relevant manipulation outcomes are indistinguishable under `g`. The identity relation is therefore indexed by the gripper-action interface.

## Why This Beats The Alternatives
- Compared with bigger models, ICIP changes the target variable.
- Compared with active perception, ICIP changes what identity means after an action channel is selected.
- Compared with affordances, ICIP separates "what action is possible" from "which object distinctions are observable and sufficient for this interface."
- Compared with a benchmark, ICIP gives a formal failure condition: non-nested partitions prevent a single identity from being both observable and sufficient.

## Evidence Required
The paper needs: a finite-partition proposition, a runnable synthetic manipulation-perception environment with multiple grippers, collision/non-nesting metrics, and planner/classifier comparisons showing that global object IDs and common gripper-agnostic labels fail in different ways.
"""
    (DOCS / "novelty_decision.md").write_text(content, encoding="utf-8")


def write_claims() -> None:
    content = """# Claims

## Supported Claims
1. In finite latent-state manipulation settings, every gripper-action observation channel induces an equivalence relation over object states.
2. If two grippers induce non-nested partitions and their task outcomes require their respective distinctions, no single gripper-agnostic identity partition can be both observable for each gripper and sufficient for each gripper's task.
3. The synthetic experiment demonstrates this failure mode for pinch, suction, and enveloping grippers: global IDs are not observable from a single gripper's channel, while the common gripper-agnostic label is observable but loses task-relevant distinctions.
4. Interface-conditioned identity partitions recover the observable and task-sufficient distinctions in the toy environment.

## Unsupported Or Only Partially Supported Claims
1. The paper does not prove the phenomenon dominates real robot datasets.
2. The paper does not introduce a new tactile sensor, gripper, or physical robot benchmark.
3. The paper does not show real-world robot trials.
4. The literature sweep is broad metadata/abstract coverage, not a verified full-PDF review of all 1000 entries.

## Formal-Claim Status
The main theorem is a finite partition impossibility result. It is proof-level in the paper if assumptions are stated exactly. The experiment is illustrative evidence, not a real-robot validation.
"""
    (DOCS / "claims.md").write_text(content, encoding="utf-8")


def write_attacks() -> None:
    content = """# Reviewer Attacks

1. **This is just affordances.** Response: affordances model action possibilities; ICIP models the identity relation induced by observability and task sufficiency for a gripper-action channel. The same affordance can still leave identity over-refined or under-refined.
2. **This is just active perception.** Response: active perception selects informative actions for a fixed latent target. ICIP asks whether the target identity relation itself changes when the action/gripper channel changes.
3. **The experiment is synthetic.** Concede. The paper should be judged as a formal/mechanistic position with runnable evidence, not as a real-robot systems paper.
4. **A universal latent state can contain all attributes.** Response: a full latent state may exist, but a gripper cannot necessarily observe it. The claim concerns deployable identity labels that are both observable and sufficient.
5. **A downstream planner could ignore irrelevant global-label distinctions.** Response: yes, and that is exactly the quotient argument; if distinctions are irrelevant/unobservable for the interface, the identity abstraction should quotient them out.
6. **Multi-modal models can fuse vision and touch.** Response: fusion still needs to model which distinctions each action-gated modality can reveal.
7. **The literature search is noisy.** Concede. Crossref produced broad coverage under rate limits; hostile papers were inspected at metadata/abstract level, and final submission would require manual full-PDF verification.
8. **No real robot.** Concede. Paper-readiness should be workshop/revise unless paired with real robot validation.
9. **The theorem is obvious.** Response: the novelty is not lattice theory alone; it is applying the observability/sufficiency conflict to object identity in gripper-dependent manipulation perception and making it operational.
10. **The name identity may confuse readers.** Response: define it operationally as a task-facing equivalence relation, not metaphysical object sameness.
"""
    (DOCS / "reviewer_attacks.md").write_text(content, encoding="utf-8")


def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    write_literature_map(rows)
    write_hostile(rows)
    write_novelty_boundary()
    write_decision()
    write_claims()
    write_attacks()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
