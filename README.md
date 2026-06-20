# 29 Gripper Dependent Object Identity

Anonymous ICLR-style paper package for:

**When the Same Object Is Not the Same: Interface-Conditioned Identity for Robot Manipulation**

## Thesis

Object identity for robot manipulation should be represented as an interface-conditioned partition, not as a single gripper-agnostic label, whenever different gripper-action channels induce distinct or non-comparable observability/task relations.

## Final Hardening Status

This is the v3 final full-scale version.

The full-scale suite evaluates:

- 373,248 latent object states.
- 7 manipulation interfaces.
- 6 regimes.
- 10 identity/control strategies.
- 156,764,160 main state-method decisions.
- 646,829,820 exact learned pair/action distribution cases.

Key results:

- Baseline visible tasks: oracle ICIP and learned ICIP reach 100.0% action success.
- Common gripper-agnostic labels reach 3.2% action success in the baseline visible regime.
- Hidden-pair tasks: naive/oracle ICIP drops to 10.7% action success.
- Active ICIP recovers 100.0% action success in hidden-pair tasks with 0.88 utility.
- Global ID reaches 100.0% only in the global-observable control, where the observability premise is changed.

The paper still does not claim real robot validation or real-world prevalence. It is submission-ready as a formal/synthetic mechanism paper with explicit boundaries.

## Reproduce Evidence

From the repository root:

```powershell
python experiments/run_icip_experiment.py
python experiments/full_scale_icip_experiment.py
```

The legacy v2 script regenerates the 96-object audit tables. The v3 full-scale script regenerates:

- `results/full_scale/main_performance.csv`
- `results/full_scale/learned_partition_recovery.csv`
- `results/full_scale/non_nesting_prevalence.csv`
- `results/full_scale/sensor_cost_phase_diagram.csv`
- `results/full_scale/cross_interface_transfer.csv`
- `results/full_scale/experiment_summary.json`
- `paper/tables/full_scale_*.tex`
- `figures/full_scale/*.pdf`

Both experiment scripts use only the Python standard library.

## Rebuild Literature Artifacts

```powershell
python scripts/literature_sweep.py
python scripts/synthesize_docs.py
```

The current literature run used Crossref because OpenAlex and Semantic Scholar returned HTTP 429 from this environment. The generated literature artifacts are checked in under `docs/` and `data/`.

## Build Paper

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The build script copies the final PDF to Downloads and removes transient local `paper/main.pdf`.

## Final PDF

- Canonical PDF: `C:/Users/wangz/Downloads/29.pdf`
- Pages: 25
- Size: 325,610 bytes
- SHA256: `9E9B16A8A9D82BC4F6ED1CFF6802454218EB9AEC44CC0158E2EBBBF46E38726D`
- Visual hardening: VLA-style one-point green citation boxes and red internal link boxes verified on pages 2, 3, and 6, with no cyan boxes.
