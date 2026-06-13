# Child Status: Paper 29

Stage: complete; v2 submission hardening ready to commit and push

Current facts:
- Literature sweep completed with `docs/related_work_matrix.csv` containing 1000 rows and `docs/hostile_prior_work.md` plus the data hostile-prior CSV.
- Main experiment generated 96 latent objects, three gripper interfaces, and 9 baseline metric rows.
- Main result: ICIP is observable and task-sufficient in the constructed baseline; common labels are observable but insufficient; global IDs are sufficient but not observable.
- V2 hidden-task stress generated `results/hidden_task_stress.csv` and `paper/tables/hidden_task_stress.tex`.
- V2 stress result: when the task needs a gripper-hidden attribute, ICIP action success drops from 100.0% to 50.0% for pinch, suction, and enveloping.
- Paper generated at `paper/main.tex` with visible v2 note, hidden-task stress table, narrowed abstract, and narrowed limitations.
- LaTeX build completed with `scripts/build_pdf.ps1`.
- Final PDF copied to `C:/Users/wangz/Downloads/29.pdf`.
- Transient `paper/main.pdf` removed so the final PDF exists only at the required Downloads path.
- Checked Desktop paths contain no `29.pdf`.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/29_gripper_dependent_object_identity`.
- `docs/final_audit.md` exists and reports build status, v2 stress evidence, Downloads-only artifact status, Desktop absence, and local PDF absence.

Commands run:
- `python experiments\run_icip_experiment.py`
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- Safe probes for build status, Downloads PDF, Desktop absence, local PDF absence, LaTeX log status, and generated stress outputs.

Historical failures:
- OpenAlex and Semantic Scholar returned HTTP 429 during literature collection; Crossref fallback recovered the matrix.
- A previous build failed on a generated table wrapper and was patched before v1.
- The first v2 build failed on `\bottomrule` after the new generated hidden-stress table; removing that wrapper rule fixed the build.

Recovery / hardening steps:
- Added v2 hidden-task stress and narrowed the ICIP claim to observable task-relevant quotients.
- Added standard hardening docs: attack log, version log, hostile reviewer response, rigor checklist, reproducibility checklist, and readiness decision.
- Added `scripts/build_pdf.ps1` and `.gitignore` rule for `paper/main.pdf`.
- Rebuilt the canonical PDF and removed the tracked local PDF.

Next:
- Commit and push the v2 hardening update.
