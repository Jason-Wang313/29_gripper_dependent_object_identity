# Child Status: Paper 29

Stage: complete; v3 final full-scale version exported, verified, ready to commit and push.

Current facts:

- Final manuscript: `paper/main.tex`.
- Canonical PDF: `C:/Users/wangz/Downloads/29.pdf`.
- PDF pages: 25.
- PDF size: 325,610 bytes.
- PDF SHA256: `9E9B16A8A9D82BC4F6ED1CFF6802454218EB9AEC44CC0158E2EBBBF46E38726D`.
- Latest visual hardening: VLA-style one-point green citation boxes and red internal link boxes verified on pages 2, 3, and 6; no cyan boxes.
- Local `paper/main.pdf` is absent after final export.
- Build status: `data/build_status.json` reports `complete`, copied `true`, removed local PDF `true`.
- Final build log scan found no overfull boxes, unresolved refs/cites, fatal errors, or undefined references.
- Public GitHub repo exists: `https://github.com/Jason-Wang313/29_gripper_dependent_object_identity`.

Full-scale v3 evidence:

- `experiments/full_scale_icip_experiment.py` completed successfully.
- Latent states: 373,248.
- Interfaces: pinch, suction, enveloping, spatula, magnetic, needle, clamp.
- Regimes: aligned control, baseline visible, hidden single, hidden pair, irrelevant hidden control, global observable control.
- Methods: global ID, common label, oracle ICIP, learned ICIP, universal refinement, universal coarsening, multimodal fusion, interface routing, active ICIP, abstaining ICIP.
- Main state-method decisions represented: 156,764,160.
- Exact learned pair/action distribution cases: 646,829,820.
- Non-nesting worlds represented: 19,200.
- Phase cells: 49.

Key results:

- Baseline oracle ICIP action success: 100.0%.
- Baseline learned ICIP action success: 100.0%.
- Baseline common-label action success: 3.2%.
- Hidden-pair oracle ICIP action success: 10.7%.
- Hidden-pair active ICIP action success: 100.0%.
- Hidden-pair active ICIP utility: 0.88.
- Global-observable global ID action success: 100.0%.

Commands run:

- `python experiments\full_scale_icip_experiment.py`
- `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` locally for QA.
- `powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1`
- `pdfinfo C:\Users\wangz\Downloads\29.pdf`
- `pdftotext C:\Users\wangz\Downloads\29.pdf -`
- `Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\29.pdf`

Historical notes:

- v2 remains as a legacy 96-object audit through `experiments/run_icip_experiment.py`.
- The v3 build required removing `\bottomrule` after some `\input` table snippets and resizing two wide appendix tables.
- The final paper explicitly avoids real-robot and prevalence overclaims.

Next:

- Commit and push the v3 final full-scale update.
