# Reproducibility Checklist

- [x] Legacy experiment script is `experiments/run_icip_experiment.py`.
- [x] Full-scale experiment script is `experiments/full_scale_icip_experiment.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Legacy outputs are `results/experiment_metrics.csv`, `results/partition_relations.csv`, `results/hidden_task_stress.csv`, and `results/experiment_summary.json`.
- [x] Full-scale outputs are under `results/full_scale/`.
- [x] Full-scale tables are `paper/tables/full_scale_*.tex`.
- [x] Full-scale figures are `figures/full_scale/*.pdf`.
- [x] Paper source is `paper/main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/29.pdf`.
- [x] Canonical PDF has 25 pages.
- [x] Canonical PDF SHA256 is `9E9B16A8A9D82BC4F6ED1CFF6802454218EB9AEC44CC0158E2EBBBF46E38726D`.
- [x] Local `paper/main.pdf` is removed after canonical copy.
- [x] Final build log scan is clean for overfull boxes, unresolved refs/cites, undefined references, and fatal errors.
- [x] VLA-style link-box policy is configured in `paper/main.tex`; final PDF has one-point green citation boxes, red internal reference boxes, and no cyan boxes.

Recommended verification commands:

```powershell
python experiments\run_icip_experiment.py
python experiments\full_scale_icip_experiment.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
pdfinfo C:\Users\wangz\Downloads\29.pdf
pdftotext C:\Users\wangz\Downloads\29.pdf -
Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\29.pdf
```
