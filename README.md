# 29 Gripper Dependent Object Identity

Anonymous ICLR-style paper package for:

**When the Same Object Is Not the Same: Interface-Conditioned Identity for Robot Manipulation**

## Thesis

Object identity for robot manipulation should be represented as an interface-conditioned partition, not as a single gripper-agnostic label, whenever different gripper-action channels induce non-nested observability relations.

## Reproduce Evidence

From the repository root:

```powershell
python experiments/run_icip_experiment.py
```

This regenerates:

- `results/experiment_metrics.csv`
- `results/partition_relations.csv`
- `results/experiment_summary.json`
- `paper/tables/experiment_metrics.tex`
- `paper/tables/partition_relations.tex`

The experiment uses only the Python standard library.

## Rebuild Literature Artifacts

```powershell
python scripts/literature_sweep.py
python scripts/synthesize_docs.py
```

The current run used Crossref because OpenAlex and Semantic Scholar returned HTTP 429 from this environment. The generated literature artifacts are checked in under `docs/` and `data/`.

## Build Paper

From `paper/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The paper uses the official ICLR 2026 style files copied into `paper/`.

## Final PDF

The compiled submission PDF for the batch is:

`C:/Users/wangz/Downloads/29.pdf`
