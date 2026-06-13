# Reproducibility Checklist

- [x] Main experiment script is `experiments/run_icip_experiment.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main outputs are `results/experiment_metrics.csv`, `results/partition_relations.csv`, and `results/experiment_summary.json`.
- [x] V2 output is `results/hidden_task_stress.csv`.
- [x] Paper tables are `paper/tables/experiment_metrics.tex`, `paper/tables/partition_relations.tex`, and `paper/tables/hidden_task_stress.tex`.
- [x] Paper source is `paper/main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/29.pdf`.
- [x] Local `paper/main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.

Recommended verification commands:

```powershell
python experiments\run_icip_experiment.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
