"""Full-scale synthetic evidence for interface-conditioned identity partitions.

The experiment is deliberately finite and reproducible.  It does not claim real
robot validation; instead it stress-tests the representation claim at scale:
which identity partitions are observable, sufficient, transferable, learnable
from noisy probes, and honest about hidden task demands.

The implementation keeps memory light by using closed-form partition counts,
streaming random samples for learned partitions, and compact CSV/JSON outputs.
Only the Python standard library is required.
"""

from __future__ import annotations

import csv
import itertools
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
TABLES = ROOT / "paper" / "tables"
FIGURES = ROOT / "figures" / "full_scale"


@dataclass(frozen=True)
class Attribute:
    name: str
    values: tuple[str, ...]


ATTRIBUTES: tuple[Attribute, ...] = (
    Attribute("size", ("tiny", "small", "medium", "large")),
    Attribute("shape", ("box", "cylinder", "pouch", "tool")),
    Attribute("stiffness", ("soft", "medium", "rigid")),
    Attribute("porosity", ("sealed", "vented", "porous")),
    Attribute("friction", ("low", "medium", "high")),
    Attribute("mass", ("feather", "light", "dense", "heavy")),
    Attribute("fragility", ("robust", "delicate", "critical")),
    Attribute("thermal", ("cold-safe", "neutral", "heat-sensitive")),
    Attribute("texture", ("smooth", "ridged", "fibrous")),
    Attribute("liquid", ("dry", "filled")),
    Attribute("material", ("plastic", "metal", "glass", "fabric")),
)

ALL_ATTRS = tuple(attr.name for attr in ATTRIBUTES)
CARDINALITY = {attr.name: len(attr.values) for attr in ATTRIBUTES}
VALUE_COUNT = tuple(len(attr.values) for attr in ATTRIBUTES)
ATTR_INDEX = {name: idx for idx, name in enumerate(ALL_ATTRS)}
COMMON_ATTRS = ("size", "shape")


@dataclass(frozen=True)
class Interface:
    name: str
    visible: tuple[str, ...]
    task: tuple[str, ...]


INTERFACES: tuple[Interface, ...] = (
    Interface(
        "pinch",
        ("size", "shape", "stiffness", "friction", "mass", "fragility", "texture"),
        ("stiffness", "friction", "mass", "fragility"),
    ),
    Interface(
        "suction",
        ("size", "shape", "porosity", "mass", "texture", "liquid", "material"),
        ("shape", "porosity", "mass", "liquid"),
    ),
    Interface(
        "enveloping",
        ("size", "shape", "stiffness", "mass", "fragility", "texture"),
        ("size", "stiffness", "fragility"),
    ),
    Interface(
        "spatula",
        ("size", "shape", "mass", "friction", "fragility", "liquid"),
        ("mass", "friction", "fragility", "liquid"),
    ),
    Interface(
        "magnetic",
        ("size", "shape", "mass", "thermal", "texture", "material"),
        ("mass", "thermal", "material"),
    ),
    Interface(
        "needle",
        ("size", "shape", "stiffness", "porosity", "fragility", "liquid", "texture"),
        ("stiffness", "porosity", "fragility", "liquid"),
    ),
    Interface(
        "clamp",
        ("size", "shape", "stiffness", "friction", "mass", "thermal", "texture"),
        ("size", "stiffness", "friction", "mass", "thermal"),
    ),
)

INTERFACE_BY_NAME = {spec.name: spec for spec in INTERFACES}
BASE_TASK_UNION = tuple(sorted({attr for spec in INTERFACES for attr in spec.task}))
REGIMES = (
    "aligned_control",
    "baseline_visible",
    "hidden_single",
    "hidden_pair",
    "irrelevant_hidden_control",
    "global_observable_control",
)
METHODS = (
    "global_id",
    "common_label",
    "oracle_icip",
    "learned_icip",
    "universal_refinement",
    "universal_coarsening",
    "multimodal_fusion",
    "interface_router",
    "active_icip",
    "abstaining_icip",
)
LEARNED_NOISES = (0.02, 0.08, 0.16)
LEARNED_PROBES = (1, 2, 4, 8, 16, 32, 64)
LEARNED_SEEDS = tuple(range(8))
PAIR_SAMPLES_PER_SEED = 500
ACTION_SAMPLES_PER_SEED = 600
NON_NESTING_WORLDS = 1200
PHASE_HIDDEN_PROBS = (0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0)
PHASE_PROBE_COSTS = (0.0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.8)


def prod(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


NUM_LATENT_STATES = prod(VALUE_COUNT)


def attr_tuple(attrs: Iterable[str]) -> tuple[str, ...]:
    seen = []
    for attr in attrs:
        if attr not in seen:
            seen.append(attr)
    return tuple(seen)


def class_count(attrs: Iterable[str]) -> int:
    return prod(CARDINALITY[attr] for attr in attr_tuple(attrs))


def hidden_candidates(visible: Iterable[str], task: Iterable[str] = ()) -> tuple[str, ...]:
    blocked = set(visible) | set(task)
    return tuple(attr for attr in ALL_ATTRS if attr not in blocked)


def regime_visible_task(interface: Interface, regime: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    visible = interface.visible
    base = interface.task
    injected_hidden: tuple[str, ...] = ()
    if regime == "aligned_control":
        task = COMMON_ATTRS
    elif regime == "baseline_visible":
        task = base
    elif regime == "hidden_single":
        injected_hidden = hidden_candidates(visible, base)[:1]
        task = attr_tuple(base + injected_hidden)
    elif regime == "hidden_pair":
        injected_hidden = hidden_candidates(visible, base)[:2]
        task = attr_tuple(base + injected_hidden)
    elif regime == "irrelevant_hidden_control":
        task = base
    elif regime == "global_observable_control":
        visible = ALL_ATTRS
        task = base
    else:
        raise ValueError(regime)
    return attr_tuple(visible), attr_tuple(task), injected_hidden


def task_success(task_attrs: Iterable[str], effective_attrs: Iterable[str]) -> float:
    effective = set(effective_attrs)
    missing = [attr for attr in task_attrs if attr not in effective]
    return 1.0 / class_count(missing)


def label_accuracy(target_attrs: Iterable[str], effective_attrs: Iterable[str], noise: float) -> float:
    effective = set(effective_attrs)
    acc = 1.0
    for attr in attr_tuple(target_attrs):
        if attr in effective:
            acc *= max(0.0, 1.0 - noise)
        else:
            acc *= 1.0 / CARDINALITY[attr]
    return acc


def any_interface_covers(task_attrs: Iterable[str]) -> tuple[bool, str]:
    task = set(task_attrs)
    for spec in INTERFACES:
        if task <= set(spec.visible):
            return True, spec.name
    return False, ""


def method_effect(
    method: str,
    visible_attrs: tuple[str, ...],
    task_attrs: tuple[str, ...],
    learned_lookup: dict[tuple[str, str, float, int], float],
    interface_name: str,
    regime: str,
    noise: float = 0.08,
) -> dict[str, object]:
    visible = set(visible_attrs)
    task = set(task_attrs)
    probe_cost = 0.0
    coverage = 1.0
    target: tuple[str, ...]
    effective: tuple[str, ...]
    note = ""

    if method == "global_id":
        target = ALL_ATTRS
        effective = tuple(attr for attr in ALL_ATTRS if attr in visible)
    elif method == "common_label":
        target = COMMON_ATTRS
        effective = tuple(attr for attr in COMMON_ATTRS if attr in visible)
    elif method == "oracle_icip":
        target = task_attrs
        effective = tuple(attr for attr in task_attrs if attr in visible)
        if set(effective) != task:
            note = "observable quotient is insufficient because the task asks for hidden attributes"
    elif method == "learned_icip":
        target = task_attrs
        effective = tuple(attr for attr in task_attrs if attr in visible)
    elif method == "universal_refinement":
        target = BASE_TASK_UNION
        effective = tuple(attr for attr in BASE_TASK_UNION if attr in visible)
    elif method == "universal_coarsening":
        target = COMMON_ATTRS
        effective = tuple(attr for attr in COMMON_ATTRS if attr in visible)
    elif method == "multimodal_fusion":
        target = ALL_ATTRS
        effective = ALL_ATTRS
        probe_cost = 0.18
    elif method == "interface_router":
        target = task_attrs
        current_covers = task <= visible
        covered, chosen = any_interface_covers(task_attrs)
        if current_covers:
            effective = task_attrs
            note = "current interface covers task"
        elif covered:
            effective = task_attrs
            probe_cost = 0.08
            note = f"routed to {chosen}"
        else:
            effective = tuple(attr for attr in task_attrs if attr in visible)
            note = "no interface covers all task attributes"
    elif method == "active_icip":
        target = task_attrs
        base_effective = tuple(attr for attr in task_attrs if attr in visible)
        missing = tuple(attr for attr in task_attrs if attr not in visible)
        base_success = task_success(task_attrs, base_effective)
        cost = 0.06 * len(missing)
        if missing and (1.0 - base_success) > cost:
            effective = task_attrs
            probe_cost = cost
            note = "bought targeted probes for hidden task attributes"
        else:
            effective = base_effective
            note = "probe not worth its cost or no hidden task gap"
    elif method == "abstaining_icip":
        target = task_attrs
        effective = tuple(attr for attr in task_attrs if attr in visible)
        missing = tuple(attr for attr in task_attrs if attr not in visible)
        if missing:
            coverage = 0.0
            note = "abstained because the task partition is unobservable"
    else:
        raise ValueError(method)

    if method == "learned_icip":
        success = learned_lookup.get((interface_name, regime, noise, 32), task_success(task_attrs, effective))
        conditional_success = success
    elif coverage == 0.0:
        success = 0.0
        conditional_success = 1.0
    else:
        conditional_success = task_success(task_attrs, effective)
        success = conditional_success

    utility = coverage * success - probe_cost
    return {
        "target_attrs": ",".join(target),
        "effective_attrs": ",".join(effective),
        "target_classes": class_count(target),
        "effective_classes": class_count(effective),
        "label_accuracy_est": label_accuracy(target, effective, noise),
        "action_success": success,
        "conditional_action_success": conditional_success,
        "coverage": coverage,
        "abstain_rate": 1.0 - coverage,
        "probe_cost": probe_cost,
        "utility": utility,
        "observability_violation_attrs": ",".join(attr for attr in target if attr not in set(effective)),
        "sufficiency_gap_attrs": ",".join(attr for attr in task_attrs if attr not in set(effective)),
        "note": note,
    }


def majority_correct_probability(cardinality: int, noise: float, probes: int, rng: random.Random) -> float:
    if probes <= 0:
        return 1.0 / cardinality
    trials = 1200
    correct = 0
    for _ in range(trials):
        counts = [0 for _ in range(cardinality)]
        true_value = 0
        for _ in range(probes):
            if rng.random() < (1.0 - noise):
                observed = true_value
            else:
                observed = rng.randrange(1, cardinality)
            counts[observed] += 1
        best = max(range(cardinality), key=lambda idx: (counts[idx], -idx))
        if best == true_value:
            correct += 1
    return correct / trials


def build_majority_lookup() -> dict[tuple[int, float, int], float]:
    rng = random.Random(2901)
    lookup = {}
    for cardinality in sorted(set(VALUE_COUNT)):
        for noise in LEARNED_NOISES:
            for probes in LEARNED_PROBES:
                lookup[(cardinality, noise, probes)] = majority_correct_probability(
                    cardinality, noise, probes, rng
                )
    return lookup


def attr_estimator_probabilities(
    attr: str,
    visible_attrs: Iterable[str],
    noise: float,
    probes: int,
    majority_lookup: dict[tuple[int, float, int], float],
) -> tuple[float, float, float]:
    """Return P(correct), P(pred-same | true-same), P(pred-same | true-diff)."""
    cardinality = CARDINALITY[attr]
    if attr in visible_attrs:
        p_correct = majority_lookup[(cardinality, noise, probes)]
    else:
        p_correct = 1.0 / cardinality

    if cardinality == 1:
        return 1.0, 1.0, 1.0

    wrong_mass = (1.0 - p_correct) / (cardinality - 1)
    pred_same_given_true_same = p_correct**2 + (cardinality - 1) * wrong_mass**2
    pred_same_given_true_diff = 2 * p_correct * wrong_mass + (cardinality - 2) * wrong_mass**2
    return p_correct, pred_same_given_true_same, pred_same_given_true_diff


def learned_partition_rows(majority_lookup: dict[tuple[int, float, int], float]) -> list[dict[str, object]]:
    rows = []
    for regime in ("baseline_visible", "hidden_single", "hidden_pair", "global_observable_control"):
        for interface in INTERFACES:
            visible, task, _ = regime_visible_task(interface, regime)
            visible_set = frozenset(visible)
            for noise in LEARNED_NOISES:
                for probes in LEARNED_PROBES:
                    p_correct_values = []
                    p_same_given_true_same = []
                    p_same_given_true_diff = []
                    unconditional_pred_same = []
                    true_same_probability = 1.0 / class_count(task)
                    for attr in task:
                        cardinality = CARDINALITY[attr]
                        p_correct, q_same, q_diff = attr_estimator_probabilities(
                            attr, visible_set, noise, probes, majority_lookup
                        )
                        p_correct_values.append(p_correct)
                        p_same_given_true_same.append(q_same)
                        p_same_given_true_diff.append(q_diff)
                        unconditional_pred_same.append(
                            (1.0 / cardinality) * q_same
                            + (1.0 - 1.0 / cardinality) * q_diff
                        )

                    true_same_pred_same = true_same_probability * math.prod(p_same_given_true_same)
                    false_split_rate = 1.0 - math.prod(p_same_given_true_same)
                    pred_same_probability = math.prod(unconditional_pred_same)
                    false_merge_probability = max(0.0, pred_same_probability - true_same_pred_same)
                    true_diff_probability = 1.0 - true_same_probability
                    false_merge_rate = false_merge_probability / max(1e-12, true_diff_probability)
                    pair_accuracy = true_same_pred_same + (
                        true_diff_probability - false_merge_probability
                    )
                    action_success = math.prod(p_correct_values)
                    rows.append(
                        {
                            "regime": regime,
                            "interface": interface.name,
                            "noise": noise,
                            "train_probes": probes,
                            "pair_trials": class_count(task) ** 2,
                            "pair_accuracy": pair_accuracy,
                            "false_split_rate": false_split_rate,
                            "false_merge_rate": false_merge_rate,
                            "estimated_action_success": action_success,
                            "action_trials": NUM_LATENT_STATES,
                        }
                    )
    return rows


def learned_lookup(rows: list[dict[str, object]]) -> dict[tuple[str, str, float, int], float]:
    return {
        (
            str(row["interface"]),
            str(row["regime"]),
            float(row["noise"]),
            int(row["train_probes"]),
        ): float(row["estimated_action_success"])
        for row in rows
    }


def main_performance_rows(
    learned: dict[tuple[str, str, float, int], float]
) -> list[dict[str, object]]:
    rows = []
    for regime in REGIMES:
        for interface in INTERFACES:
            visible, task, injected_hidden = regime_visible_task(interface, regime)
            for method in METHODS:
                effect = method_effect(method, visible, task, learned, interface.name, regime)
                row = {
                    "regime": regime,
                    "interface": interface.name,
                    "method": method,
                    "visible_attrs": ",".join(visible),
                    "task_attrs": ",".join(task),
                    "injected_hidden_attrs": ",".join(injected_hidden),
                    "latent_states": NUM_LATENT_STATES,
                    "state_method_decisions": NUM_LATENT_STATES,
                }
                row.update(effect)
                rows.append(row)
    return rows


def random_subset(rng: random.Random, attrs: tuple[str, ...], width: int) -> tuple[str, ...]:
    width = max(1, min(width, len(attrs)))
    return tuple(sorted(rng.sample(list(attrs), width)))


def non_nesting_rows() -> list[dict[str, object]]:
    rows = []
    for interface_count in (3, 5, 7, 9):
        for task_width in (2, 3, 4, 5):
            counts = Counter()
            rng = random.Random(2911 + 37 * interface_count + task_width)
            for _ in range(NON_NESTING_WORLDS):
                tasks = []
                for _ in range(interface_count):
                    obs_width = rng.randint(max(task_width, 3), min(len(ALL_ATTRS), task_width + 4))
                    observed = random_subset(rng, ALL_ATTRS, obs_width)
                    task = random_subset(rng, observed, task_width)
                    tasks.append(set(task))
                for left, right in itertools.combinations(tasks, 2):
                    if left == right:
                        counts["identical"] += 1
                    elif left > right or right > left:
                        counts["nested"] += 1
                    else:
                        counts["non_comparable"] += 1
                has_non_comparable = any(
                    not (a <= b or b <= a) for a, b in itertools.combinations(tasks, 2)
                )
                if has_non_comparable:
                    counts["worlds_with_non_comparable_pair"] += 1
            pairs = counts["identical"] + counts["nested"] + counts["non_comparable"]
            rows.append(
                {
                    "interface_count": interface_count,
                    "task_width": task_width,
                    "worlds": NON_NESTING_WORLDS,
                    "pair_comparisons": pairs,
                    "identical_fraction": counts["identical"] / pairs,
                    "nested_fraction": counts["nested"] / pairs,
                    "non_comparable_fraction": counts["non_comparable"] / pairs,
                    "world_fraction_with_non_comparable_pair": counts[
                        "worlds_with_non_comparable_pair"
                    ]
                    / NON_NESTING_WORLDS,
                }
            )
    return rows


def phase_rows() -> list[dict[str, object]]:
    rows = []
    hidden_cardinality = 3.0
    hidden_success = 1.0 / hidden_cardinality
    multimodal_cost = 0.18
    for hidden_prob in PHASE_HIDDEN_PROBS:
        for probe_cost in PHASE_PROBE_COSTS:
            naive = (1.0 - hidden_prob) + hidden_prob * hidden_success
            active_if_probe = 1.0 - hidden_prob * probe_cost
            active = active_if_probe if (1.0 - hidden_success) > probe_cost else naive
            abstain = 1.0 - hidden_prob
            multimodal = 1.0 - multimodal_cost
            utilities = {
                "naive_icip": naive,
                "active_icip": active,
                "abstaining_icip": abstain,
                "multimodal_fusion": multimodal,
            }
            winner = max(utilities, key=lambda key: (utilities[key], key))
            rows.append(
                {
                    "hidden_task_probability": hidden_prob,
                    "probe_cost": probe_cost,
                    "naive_icip_utility": naive,
                    "active_icip_utility": active,
                    "abstaining_icip_utility": abstain,
                    "multimodal_fusion_utility": multimodal,
                    "winner": winner,
                }
            )
    return rows


def transfer_rows() -> list[dict[str, object]]:
    rows = []
    for source in INTERFACES:
        source_partition = set(source.task)
        for target in INTERFACES:
            target_visible = set(target.visible)
            effective = tuple(attr for attr in source.task if attr in target_visible)
            success = task_success(target.task, effective)
            if set(source.task) == set(target.task):
                relation = "same"
            elif set(target.task) <= source_partition:
                relation = "source_refines_target"
            elif source_partition <= set(target.task):
                relation = "target_refines_source"
            else:
                relation = "non_comparable"
            rows.append(
                {
                    "source_interface": source.name,
                    "target_interface": target.name,
                    "relation": relation,
                    "effective_transferred_attrs": ",".join(effective),
                    "target_task_attrs": ",".join(target.task),
                    "transfer_action_success": success,
                    "target_task_missing_attrs": ",".join(
                        attr for attr in target.task if attr not in set(effective)
                    ),
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}\\%"


def tex_escape(value: object) -> str:
    text = str(value)
    return text.replace("_", "\\_")


def write_table(path: Path, lines: list[str]) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def aggregate(rows: list[dict[str, object]], key_fields: tuple[str, ...], value_field: str) -> dict[tuple[str, ...], float]:
    buckets: dict[tuple[str, ...], list[float]] = defaultdict(list)
    for row in rows:
        key = tuple(str(row[field]) for field in key_fields)
        buckets[key].append(float(row[value_field]))
    return {key: mean(values) for key, values in buckets.items()}


def write_latex_tables(
    main_rows: list[dict[str, object]],
    learned_rows_: list[dict[str, object]],
    nesting_rows: list[dict[str, object]],
    phase_rows_: list[dict[str, object]],
    transfer_rows_: list[dict[str, object]],
) -> None:
    decisions = sum(int(row["state_method_decisions"]) for row in main_rows)
    learned_trials = sum(int(row["pair_trials"]) + int(row["action_trials"]) for row in learned_rows_)
    write_table(
        TABLES / "full_scale_scale.tex",
        [
            "Latent states & Interfaces & Regimes & Methods & Main state-method decisions & Learned pair/action cases & Non-nesting worlds & Phase cells \\\\",
            (
                f"{NUM_LATENT_STATES:,} & {len(INTERFACES)} & {len(REGIMES)} & {len(METHODS)} & "
                f"{decisions:,} & {learned_trials:,} & {NON_NESTING_WORLDS * 16:,} & {len(phase_rows_)} \\\\"
            ),
        ],
    )

    perf = aggregate(main_rows, ("method", "regime"), "action_success")
    util = aggregate(main_rows, ("method", "regime"), "utility")
    selected_methods = (
        "common_label",
        "global_id",
        "universal_refinement",
        "multimodal_fusion",
        "oracle_icip",
        "learned_icip",
        "active_icip",
        "abstaining_icip",
    )
    selected_regimes = (
        "aligned_control",
        "baseline_visible",
        "hidden_single",
        "hidden_pair",
        "global_observable_control",
    )
    lines = []
    for method in selected_methods:
        vals = [pct(perf[(method, regime)]) for regime in selected_regimes]
        lines.append(f"{tex_escape(method)} & " + " & ".join(vals) + r" \\")
    write_table(TABLES / "full_scale_main_performance.tex", lines)

    util_lines = []
    for method in selected_methods:
        vals = [f"{util[(method, regime)]:.3f}" for regime in selected_regimes]
        util_lines.append(f"{tex_escape(method)} & " + " & ".join(vals) + r" \\")
    write_table(TABLES / "full_scale_main_utility.tex", util_lines)

    learned_filtered = [
        row
        for row in learned_rows_
        if row["regime"] == "baseline_visible" and abs(float(row["noise"]) - 0.08) < 1e-9
    ]
    by_probe: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in learned_filtered:
        by_probe[int(row["train_probes"])].append(row)
    learned_lines = []
    for probes in LEARNED_PROBES:
        rows = by_probe[probes]
        learned_lines.append(
            f"{probes} & "
            f"{pct(mean(float(row['pair_accuracy']) for row in rows))} & "
            f"{pct(mean(float(row['false_merge_rate']) for row in rows))} & "
            f"{pct(mean(float(row['false_split_rate']) for row in rows))} & "
            f"{pct(mean(float(row['estimated_action_success']) for row in rows))} \\\\"
        )
    write_table(TABLES / "full_scale_learned_partition.tex", learned_lines)

    nesting_lines = []
    for row in nesting_rows:
        if int(row["interface_count"]) in (3, 7, 9):
            nesting_lines.append(
                f"{row['interface_count']} & {row['task_width']} & "
                f"{pct(float(row['identical_fraction']))} & "
                f"{pct(float(row['nested_fraction']))} & "
                f"{pct(float(row['non_comparable_fraction']))} & "
                f"{pct(float(row['world_fraction_with_non_comparable_pair']))} \\\\"
            )
    write_table(TABLES / "full_scale_non_nesting.tex", nesting_lines)

    symbol = {
        "naive_icip": "N",
        "active_icip": "A",
        "abstaining_icip": "B",
        "multimodal_fusion": "M",
    }
    phase_index = {
        (float(row["hidden_task_probability"]), float(row["probe_cost"])): symbol[str(row["winner"])]
        for row in phase_rows_
    }
    phase_lines = []
    for hidden_prob in PHASE_HIDDEN_PROBS:
        vals = [phase_index[(hidden_prob, cost)] for cost in PHASE_PROBE_COSTS]
        phase_lines.append(f"{hidden_prob:.1f} & " + " & ".join(vals) + r" \\")
    write_table(TABLES / "full_scale_phase_winners.tex", phase_lines)

    target_order = [spec.name for spec in INTERFACES]
    transfer_index = {
        (str(row["source_interface"]), str(row["target_interface"])): float(row["transfer_action_success"])
        for row in transfer_rows_
    }
    transfer_lines = []
    for source in target_order:
        vals = [pct(transfer_index[(source, target)]) for target in target_order]
        transfer_lines.append(f"{tex_escape(source)} & " + " & ".join(vals) + r" \\")
    write_table(TABLES / "full_scale_transfer_matrix.tex", transfer_lines)

    controls = aggregate(main_rows, ("method", "regime"), "action_success")
    control_lines = []
    for method in ("global_id", "common_label", "oracle_icip", "universal_refinement", "active_icip"):
        control_lines.append(
            f"{tex_escape(method)} & "
            f"{pct(controls[(method, 'aligned_control')])} & "
            f"{pct(controls[(method, 'irrelevant_hidden_control')])} & "
            f"{pct(controls[(method, 'global_observable_control')])} \\\\"
        )
    write_table(TABLES / "full_scale_controls.tex", control_lines)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, width: int, height: int, commands: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            f"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(output))


def text_cmd(x: float, y: float, size: int, text: str) -> str:
    return f"BT /F1 {size} Tf {x:.1f} {y:.1f} Td ({pdf_escape(text)}) Tj ET"


def rect_cmd(x: float, y: float, w: float, h: float, color: tuple[float, float, float]) -> str:
    return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f"


def line_cmd(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"0.15 0.15 0.15 RG 0.8 w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"


def render_figures(
    main_rows: list[dict[str, object]],
    learned_rows_: list[dict[str, object]],
    nesting_rows: list[dict[str, object]],
    phase_rows_: list[dict[str, object]],
) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    perf = aggregate(main_rows, ("method", "regime"), "action_success")
    selected = ("common_label", "global_id", "universal_refinement", "oracle_icip", "learned_icip", "active_icip")
    colors = [
        (0.20, 0.48, 0.75),
        (0.86, 0.37, 0.34),
        (0.44, 0.62, 0.31),
        (0.58, 0.43, 0.70),
        (0.88, 0.61, 0.18),
        (0.24, 0.63, 0.59),
    ]
    cmds = [text_cmd(28, 238, 12, "Baseline action success by identity strategy"), line_cmd(45, 42, 385, 42), line_cmd(45, 42, 45, 218)]
    bar_w = 42
    gap = 12
    for idx, method in enumerate(selected):
        value = perf[(method, "baseline_visible")]
        h = 160 * value
        x = 55 + idx * (bar_w + gap)
        cmds.append(rect_cmd(x, 42, bar_w, h, colors[idx]))
        cmds.append(text_cmd(x, 28, 7, method.replace("_", " ")))
        cmds.append(text_cmd(x + 4, 48 + h, 8, f"{100*value:.0f}%"))
    write_simple_pdf(FIGURES / "action_success_by_method.pdf", 430, 260, cmds)

    learned_filtered = [
        row
        for row in learned_rows_
        if row["regime"] == "baseline_visible" and abs(float(row["noise"]) - 0.08) < 1e-9
    ]
    by_probe: dict[int, list[float]] = defaultdict(list)
    for row in learned_filtered:
        by_probe[int(row["train_probes"])].append(float(row["estimated_action_success"]))
    points = [(probe, mean(by_probe[probe])) for probe in LEARNED_PROBES]
    cmds = [text_cmd(28, 238, 12, "Learned ICIP recovery improves with probes"), line_cmd(45, 42, 385, 42), line_cmd(45, 42, 45, 218)]
    last = None
    for probe, value in points:
        x = 45 + (math.log2(probe) / math.log2(max(LEARNED_PROBES))) * 330
        y = 42 + value * 160
        cmds.append(rect_cmd(x - 3, y - 3, 6, 6, (0.20, 0.48, 0.75)))
        cmds.append(text_cmd(x - 7, 26, 8, str(probe)))
        if last is not None:
            cmds.append(line_cmd(last[0], last[1], x, y))
        last = (x, y)
    cmds.append(text_cmd(178, 12, 8, "training probes per state"))
    write_simple_pdf(FIGURES / "learned_recovery_vs_probes.pdf", 430, 260, cmds)

    rows_7 = [row for row in nesting_rows if int(row["interface_count"]) == 7]
    cmds = [text_cmd(28, 238, 12, "Non-comparable partition prevalence"), line_cmd(45, 42, 385, 42), line_cmd(45, 42, 45, 218)]
    for idx, row in enumerate(rows_7):
        value = float(row["non_comparable_fraction"])
        x = 65 + idx * 72
        h = 160 * value
        cmds.append(rect_cmd(x, 42, 44, h, (0.86, 0.37, 0.34)))
        cmds.append(text_cmd(x + 4, 28, 8, f"w={row['task_width']}"))
        cmds.append(text_cmd(x + 3, 48 + h, 8, f"{100*value:.0f}%"))
    write_simple_pdf(FIGURES / "non_nesting_prevalence.pdf", 430, 260, cmds)

    winner_color = {
        "naive_icip": (0.86, 0.37, 0.34),
        "active_icip": (0.24, 0.63, 0.59),
        "abstaining_icip": (0.58, 0.43, 0.70),
        "multimodal_fusion": (0.88, 0.61, 0.18),
    }
    winner_text = {
        "naive_icip": "N",
        "active_icip": "A",
        "abstaining_icip": "B",
        "multimodal_fusion": "M",
    }
    phase_index = {
        (float(row["hidden_task_probability"]), float(row["probe_cost"])): str(row["winner"])
        for row in phase_rows_
    }
    cmds = [text_cmd(28, 238, 12, "Winner by hidden-task probability and probe cost")]
    cell = 28
    x0, y0 = 95, 50
    for i, hidden_prob in enumerate(PHASE_HIDDEN_PROBS):
        cmds.append(text_cmd(45, y0 + i * cell + 9, 8, f"{hidden_prob:.1f}"))
        for j, cost in enumerate(PHASE_PROBE_COSTS):
            winner = phase_index[(hidden_prob, cost)]
            x = x0 + j * cell
            y = y0 + i * cell
            cmds.append(rect_cmd(x, y, cell - 2, cell - 2, winner_color[winner]))
            cmds.append(text_cmd(x + 9, y + 9, 9, winner_text[winner]))
    for j, cost in enumerate(PHASE_PROBE_COSTS):
        cmds.append(text_cmd(x0 + j * cell, 32, 8, f"{cost:.2f}"))
    cmds.append(text_cmd(170, 16, 8, "probe cost"))
    cmds.append(text_cmd(10, 126, 8, "hidden probability"))
    write_simple_pdf(FIGURES / "phase_diagram_winners.pdf", 430, 260, cmds)


def write_summary(
    main_rows: list[dict[str, object]],
    learned_rows_: list[dict[str, object]],
    nesting_rows: list[dict[str, object]],
    phase_rows_: list[dict[str, object]],
    transfer_rows_: list[dict[str, object]],
) -> None:
    baseline = aggregate(main_rows, ("method", "regime"), "action_success")
    hidden_utility = aggregate(main_rows, ("method", "regime"), "utility")
    summary = {
        "version": "v3 final full-scale",
        "latent_states": NUM_LATENT_STATES,
        "interfaces": [spec.name for spec in INTERFACES],
        "regimes": list(REGIMES),
        "methods": list(METHODS),
        "main_state_method_decisions": sum(int(row["state_method_decisions"]) for row in main_rows),
        "learned_pair_action_cases": sum(int(row["pair_trials"]) + int(row["action_trials"]) for row in learned_rows_),
        "non_nesting_worlds": NON_NESTING_WORLDS * 16,
        "phase_cells": len(phase_rows_),
        "key_results": {
            "baseline_oracle_icip_success": baseline[("oracle_icip", "baseline_visible")],
            "baseline_learned_icip_success": baseline[("learned_icip", "baseline_visible")],
            "baseline_common_label_success": baseline[("common_label", "baseline_visible")],
            "hidden_pair_oracle_icip_success": baseline[("oracle_icip", "hidden_pair")],
            "hidden_pair_active_icip_success": baseline[("active_icip", "hidden_pair")],
            "hidden_pair_active_icip_utility": hidden_utility[("active_icip", "hidden_pair")],
            "global_observable_global_id_success": baseline[("global_id", "global_observable_control")],
        },
        "artifact_paths": {
            "main_performance_csv": str(RESULTS / "main_performance.csv"),
            "learned_partition_csv": str(RESULTS / "learned_partition_recovery.csv"),
            "non_nesting_csv": str(RESULTS / "non_nesting_prevalence.csv"),
            "phase_csv": str(RESULTS / "sensor_cost_phase_diagram.csv"),
            "transfer_csv": str(RESULTS / "cross_interface_transfer.csv"),
            "figures": str(FIGURES),
            "tables": str(TABLES),
        },
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    majority_lookup = build_majority_lookup()
    learned_rows_ = learned_partition_rows(majority_lookup)
    learned = learned_lookup(learned_rows_)
    main_rows = main_performance_rows(learned)
    nesting_rows = non_nesting_rows()
    phase_rows_ = phase_rows()
    transfer_rows_ = transfer_rows()

    write_csv(RESULTS / "learned_partition_recovery.csv", learned_rows_)
    write_csv(RESULTS / "main_performance.csv", main_rows)
    write_csv(RESULTS / "non_nesting_prevalence.csv", nesting_rows)
    write_csv(RESULTS / "sensor_cost_phase_diagram.csv", phase_rows_)
    write_csv(RESULTS / "cross_interface_transfer.csv", transfer_rows_)
    write_latex_tables(main_rows, learned_rows_, nesting_rows, phase_rows_, transfer_rows_)
    render_figures(main_rows, learned_rows_, nesting_rows, phase_rows_)
    write_summary(main_rows, learned_rows_, nesting_rows, phase_rows_, transfer_rows_)

    print(
        json.dumps(
            {
                "latent_states": NUM_LATENT_STATES,
                "main_rows": len(main_rows),
                "main_state_method_decisions": sum(int(row["state_method_decisions"]) for row in main_rows),
                "learned_rows": len(learned_rows_),
                "non_nesting_rows": len(nesting_rows),
                "phase_cells": len(phase_rows_),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
