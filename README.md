# 29 Gripper Dependent Object Identity

Anonymous ICLR-style paper package for:

**When the Same Object Is Not the Same: Interface-Conditioned Identity for Robot Manipulation**

## Thesis

Object identity for robot manipulation should be represented as an interface-conditioned partition, not as a single gripper-agnostic label, whenever different gripper-action channels induce non-nested observability relations.

## Hardening Status

This is the v2 submission-hardened version. The added hidden-task stress shows
the deployment boundary: when each gripper's task is changed to require one
attribute outside its observation channel, ICIP action success drops from
100.0% to 50.0% for pinch, suction, and enveloping.

## Reproduce Evidence

From the repository root:

```powershell
python experiments/run_icip_experiment.py
```

This regenerates:

- `results/experiment_metrics.csv`
- `results/partition_relations.csv`
- `results/hidden_task_stress.csv`
- `results/experiment_summary.json`
- `paper/tables/experiment_metrics.tex`
- `paper/tables/partition_relations.tex`
- `paper/tables/hidden_task_stress.tex`

The experiment uses only the Python standard library.

## Rebuild Literature Artifacts

```powershell
python scripts/literature_sweep.py
python scripts/synthesize_docs.py
```

The current run used Crossref because OpenAlex and Semantic Scholar returned HTTP 429 from this environment. The generated literature artifacts are checked in under `docs/` and `data/`.

## Build Paper

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The build script copies the final PDF to Downloads and removes the transient
local `paper/main.pdf`.

## Final PDF

The compiled submission PDF for the batch is:

`C:/Users/wangz/Downloads/29.pdf`
