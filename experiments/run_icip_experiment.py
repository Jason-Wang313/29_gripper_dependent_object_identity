"""Runnable evidence for interface-conditioned identity partitions.

This script creates a finite manipulation-perception toy world with three
grippers. Each gripper observes a different quotient of the latent object
state. The experiment measures the conflict between global object identity,
the common gripper-agnostic label, and the interface-conditioned quotient.
It uses only the Python standard library.
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
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
TABLES = ROOT / "paper" / "tables"


SIZES = ["small", "medium", "large"]
SHAPES = ["box", "cylinder"]
STIFFNESS = ["soft", "rigid"]
POROSITY = ["sealed", "porous"]
FRICTION = ["low", "high"]
MASS = ["light", "heavy"]

SIZE_VAL = {"small": 0.0, "medium": 0.5, "large": 1.0}
BINARY_VAL = {
    "box": 0.0,
    "cylinder": 1.0,
    "soft": 0.0,
    "rigid": 1.0,
    "sealed": 0.0,
    "porous": 1.0,
    "low": 0.0,
    "high": 1.0,
    "light": 0.0,
    "heavy": 1.0,
}


@dataclass(frozen=True)
class Obj:
    size: str
    shape: str
    stiffness: str
    porosity: str
    friction: str
    mass: str

    def global_id(self) -> str:
        return "|".join([self.size, self.shape, self.stiffness, self.porosity, self.friction, self.mass])

    def common_id(self) -> str:
        return "|".join([self.size, self.shape])


GRIPPER_FEATURES = {
    "pinch": ["size", "shape", "stiffness", "friction", "mass"],
    "suction": ["size", "shape", "porosity", "mass"],
    "enveloping": ["size", "shape", "stiffness"],
}


def all_objects() -> list[Obj]:
    return [
        Obj(*items)
        for items in itertools.product(SIZES, SHAPES, STIFFNESS, POROSITY, FRICTION, MASS)
    ]


def attr_value(obj: Obj, attr: str) -> float:
    if attr == "size":
        return SIZE_VAL[obj.size]
    return BINARY_VAL[getattr(obj, attr)]


def quotient_id(obj: Obj, gripper: str) -> str:
    return "|".join(getattr(obj, attr) for attr in GRIPPER_FEATURES[gripper])


def label_fn(kind: str, gripper: str) -> Callable[[Obj], str]:
    if kind == "global":
        return lambda obj: obj.global_id()
    if kind == "common":
        return lambda obj: obj.common_id()
    if kind == "icip":
        return lambda obj: quotient_id(obj, gripper)
    raise ValueError(kind)


def observe(obj: Obj, gripper: str, rng: random.Random, noise: float = 0.045) -> tuple[float, ...]:
    visible = set(GRIPPER_FEATURES[gripper])
    vector = []
    for attr in ["size", "shape", "stiffness", "porosity", "friction", "mass"]:
        if attr in visible:
            base = attr_value(obj, attr)
        else:
            base = 0.5 + rng.gauss(0.0, 0.12)
        vector.append(max(0.0, min(1.0, base + rng.gauss(0.0, noise))))
    return tuple(vector)


def optimal_action(obj: Obj, gripper: str) -> str:
    if gripper == "pinch":
        force = "gentle" if obj.stiffness == "soft" and obj.mass == "light" else "firm"
        pad = "sticky-pad" if obj.friction == "low" else "plain-pad"
        return f"{force}/{pad}"
    if gripper == "suction":
        pressure = "high-vacuum" if obj.porosity == "porous" or obj.mass == "heavy" else "low-vacuum"
        cup = "flat-cup" if obj.shape == "box" else "curved-cup"
        return f"{pressure}/{cup}"
    if gripper == "enveloping":
        closure = {"small": "narrow", "medium": "mid", "large": "wide"}[obj.size]
        speed = "slow" if obj.stiffness == "soft" else "normal"
        return f"{closure}/{speed}"
    raise ValueError(gripper)


def fit_centroids(samples: list[tuple[tuple[float, ...], str]]) -> dict[str, tuple[float, ...]]:
    sums: dict[str, list[float]] = {}
    counts: Counter[str] = Counter()
    for vector, label in samples:
        if label not in sums:
            sums[label] = [0.0 for _ in vector]
        for idx, value in enumerate(vector):
            sums[label][idx] += value
        counts[label] += 1
    return {label: tuple(value / counts[label] for value in values) for label, values in sums.items()}


def predict(centroids: dict[str, tuple[float, ...]], vector: tuple[float, ...]) -> str:
    best_label = ""
    best_dist = float("inf")
    for label, center in centroids.items():
        dist = sum((a - b) ** 2 for a, b in zip(vector, center))
        if dist < best_dist:
            best_dist = dist
            best_label = label
    return best_label


def majority_actions(
    objects: list[Obj],
    labels: list[str],
    gripper: str,
    action_fn: Callable[[Obj, str], str] = optimal_action,
) -> dict[str, str]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    for obj, label in zip(objects, labels):
        buckets[label][action_fn(obj, gripper)] += 1
    return {label: counter.most_common(1)[0][0] for label, counter in buckets.items()}


def partition_groups(objects: list[Obj], gripper: str) -> dict[str, list[Obj]]:
    groups: dict[str, list[Obj]] = defaultdict(list)
    for obj in objects:
        groups[quotient_id(obj, gripper)].append(obj)
    return groups


def bayes_global_upper_bound(objects: list[Obj], gripper: str) -> float:
    groups = partition_groups(objects, gripper)
    return sum(1 for _ in groups) / len(objects)


def collapsed_global_pairs(objects: list[Obj], gripper: str) -> int:
    total = 0
    for group in partition_groups(objects, gripper).values():
        n = len(group)
        total += n * (n - 1) // 2
    return total


def refines(objects: list[Obj], g_a: str, g_b: str) -> bool:
    for left, right in itertools.combinations(objects, 2):
        if quotient_id(left, g_a) == quotient_id(right, g_a):
            if quotient_id(left, g_b) != quotient_id(right, g_b):
                return False
    return True


def hidden_task_attribute(gripper: str) -> str:
    if gripper == "pinch":
        return "porosity"
    if gripper == "suction":
        return "friction"
    if gripper == "enveloping":
        return "mass"
    raise ValueError(gripper)


def hidden_task_action(obj: Obj, gripper: str) -> str:
    hidden_attr = hidden_task_attribute(gripper)
    return f"{optimal_action(obj, gripper)}/hidden-{hidden_attr}={getattr(obj, hidden_attr)}"


def evaluate(
    gripper: str,
    kind: str,
    objects: list[Obj],
    rng: random.Random,
    action_fn: Callable[[Obj, str], str] = optimal_action,
) -> dict[str, object]:
    labels = label_fn(kind, gripper)
    train_samples: list[tuple[tuple[float, ...], str]] = []
    train_objects: list[Obj] = []
    train_labels: list[str] = []
    test_samples: list[tuple[tuple[float, ...], Obj, str]] = []

    for obj in objects:
        for _ in range(10):
            label = labels(obj)
            train_samples.append((observe(obj, gripper, rng), label))
            train_objects.append(obj)
            train_labels.append(label)
        for _ in range(5):
            test_samples.append((observe(obj, gripper, rng), obj, labels(obj)))

    centroids = fit_centroids(train_samples)
    action_by_label = majority_actions(train_objects, train_labels, gripper, action_fn)

    correct = 0
    action_success = 0
    for vector, obj, true_label in test_samples:
        pred = predict(centroids, vector)
        if pred == true_label:
            correct += 1
        if action_by_label.get(pred) == action_fn(obj, gripper):
            action_success += 1

    return {
        "gripper": gripper,
        "label_scheme": kind,
        "classes": len(set(labels(obj) for obj in objects)),
        "label_accuracy": correct / len(test_samples),
        "action_success": action_success / len(test_samples),
        "global_bayes_upper_bound": bayes_global_upper_bound(objects, gripper),
        "collapsed_global_pairs": collapsed_global_pairs(objects, gripper),
    }


def evaluate_hidden_task_stress(
    objects: list[Obj],
    baseline_metrics: list[dict[str, object]],
    rng: random.Random,
) -> list[dict[str, object]]:
    baseline = {
        (str(row["gripper"]), str(row["label_scheme"])): float(row["action_success"])
        for row in baseline_metrics
    }
    rows = []
    for gripper in GRIPPER_FEATURES:
        for kind in ["global", "common", "icip"]:
            result = evaluate(gripper, kind, objects, rng, hidden_task_action)
            base = baseline[(gripper, kind)]
            hidden_success = float(result["action_success"])
            rows.append(
                {
                    "gripper": gripper,
                    "label_scheme": kind,
                    "hidden_required_attribute": hidden_task_attribute(gripper),
                    "baseline_action_success": base,
                    "hidden_task_action_success": hidden_success,
                    "action_success_drop": base - hidden_success,
                }
            )
    return rows


def write_metrics(metrics: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / "experiment_metrics.csv"
    fields = [
        "gripper",
        "label_scheme",
        "classes",
        "label_accuracy",
        "action_success",
        "global_bayes_upper_bound",
        "collapsed_global_pairs",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in metrics:
            writer.writerow(row)


def write_relations(objects: list[Obj]) -> list[dict[str, object]]:
    rows = []
    grippers = list(GRIPPER_FEATURES)
    for g_a, g_b in itertools.permutations(grippers, 2):
        rows.append({"partition_a": g_a, "partition_b": g_b, "a_refines_b": refines(objects, g_a, g_b)})
    path = RESULTS / "partition_relations.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["partition_a", "partition_b", "a_refines_b"])
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_hidden_task_stress(rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / "hidden_task_stress.csv"
    fields = [
        "gripper",
        "label_scheme",
        "hidden_required_attribute",
        "baseline_action_success",
        "hidden_task_action_success",
        "action_success_drop",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}\\%"


def latex_table_metrics(metrics: list[dict[str, object]]) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    rows = []
    order = {"global": 0, "common": 1, "icip": 2}
    for row in sorted(metrics, key=lambda r: (str(r["gripper"]), order[str(r["label_scheme"])])):
        scheme = {"global": "Global ID", "common": "Common label", "icip": "ICIP"}[str(row["label_scheme"])]
        rows.append(
            " & ".join(
                [
                    str(row["gripper"]).title(),
                    scheme,
                    str(row["classes"]),
                    pct(float(row["label_accuracy"])),
                    pct(float(row["action_success"])),
                    pct(float(row["global_bayes_upper_bound"])),
                ]
            )
            + r" \\"
        )
    content = "\n".join(rows)
    (TABLES / "experiment_metrics.tex").write_text(content + "\n", encoding="utf-8")


def latex_table_relations(relations: list[dict[str, object]]) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    selected = [row for row in relations if str(row["partition_a"]) < str(row["partition_b"])]
    rows = []
    for row in selected:
        a = str(row["partition_a"]).title()
        b = str(row["partition_b"]).title()
        a_ref_b = "yes" if refines(all_objects(), str(row["partition_a"]), str(row["partition_b"])) else "no"
        b_ref_a = "yes" if refines(all_objects(), str(row["partition_b"]), str(row["partition_a"])) else "no"
        rows.append(f"{a} vs. {b} & {a_ref_b} & {b_ref_a} \\\\")
    (TABLES / "partition_relations.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")


def latex_table_hidden_task_stress(rows: list[dict[str, object]]) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    order = {"global": 0, "common": 1, "icip": 2}
    gripper_order = {"pinch": 0, "suction": 1, "enveloping": 2}
    lines = []
    for row in sorted(rows, key=lambda r: (gripper_order[str(r["gripper"])], order[str(r["label_scheme"])])):
        scheme = {"global": "Global ID", "common": "Common label", "icip": "ICIP"}[str(row["label_scheme"])]
        lines.append(
            " & ".join(
                [
                    str(row["gripper"]).title(),
                    scheme,
                    str(row["hidden_required_attribute"]),
                    pct(float(row["baseline_action_success"])),
                    pct(float(row["hidden_task_action_success"])),
                    pct(float(row["action_success_drop"])),
                ]
            )
            + r" \\"
        )
    (TABLES / "hidden_task_stress.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rng = random.Random(29)
    objects = all_objects()
    metrics = []
    for gripper in GRIPPER_FEATURES:
        for kind in ["global", "common", "icip"]:
            metrics.append(evaluate(gripper, kind, objects, rng))

    write_metrics(metrics)
    relations = write_relations(objects)
    hidden_stress = evaluate_hidden_task_stress(objects, metrics, rng)
    write_hidden_task_stress(hidden_stress)
    latex_table_metrics(metrics)
    latex_table_relations(relations)
    latex_table_hidden_task_stress(hidden_stress)

    summary = {
        "num_latent_objects": len(objects),
        "grippers": GRIPPER_FEATURES,
        "metrics": metrics,
        "relations": relations,
        "hidden_task_stress": hidden_stress,
        "interpretation": (
            "Global identity is sufficient but not observable under each single gripper "
            "channel; the common gripper-agnostic label is observable but loses task "
            "distinctions; ICIP is both observable and sufficient in this constructed world. "
            "The hidden-task stress shows that ICIP also fails when the task requires an "
            "attribute the interface cannot observe."
        ),
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"metrics_rows": len(metrics), "objects": len(objects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
