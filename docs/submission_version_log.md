# Submission Version Log

## v3 - 2026-06-15

- Added `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `experiments/full_scale_icip_experiment.py`.
- Generated full-scale CSV outputs under `results/full_scale/`.
- Generated full-scale table snippets under `paper/tables/full_scale_*.tex`.
- Generated PDF figures under `figures/full_scale/`.
- Rewrote `paper/main.tex` into a 25-page v3 final full-scale manuscript.
- Added learned partition estimation, non-nesting prevalence, hidden single/pair stress, active sensing, abstention, multimodal fusion, interface routing, transfer, negative controls, and appendices.
- Final canonical PDF exported to `C:/Users/wangz/Downloads/29.pdf`.
- Verified the v3 final PDF hash before the later visual-hardening rebuild.

## v4 Visual Hardening - 2026-06-20

- Added the VLA role-model `hyperref` box policy to `paper/main.tex`.
- Rebuilt the canonical Downloads PDF.
- Verified 25 pages, size 325,610 bytes, SHA256 `9E9B16A8A9D82BC4F6ED1CFF6802454218EB9AEC44CC0158E2EBBBF46E38726D`, and no local `paper/main.pdf`.
- Verified one-point green citation boxes on pages 2 and 3; red internal link boxes on pages 3 and 6; and no cyan boxes.

## v2 - 2026-06-13

- Added hidden-task stress generation to `experiments/run_icip_experiment.py`.
- Generated `results/hidden_task_stress.csv`.
- Generated `paper/tables/hidden_task_stress.tex`.
- Updated the manuscript with a visible v2 note, hidden-task stress table, narrowed abstract, and stronger limitations.
- Added `scripts/build_pdf.ps1` to build, copy to Downloads, and remove local `paper/main.pdf`.

## v1 - 2026-06-11

- Initial interface-conditioned identity paper package with literature sweep, synthetic partition evidence, ICLR-style manuscript, final audit, canonical Downloads PDF, and public GitHub repo.
