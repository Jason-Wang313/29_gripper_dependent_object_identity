# Plan

## Objective
Produce an honest, runnable robotics/embodied-intelligence paper package for paper 29, starting from the seed "Gripper Dependent Object Identity" but allowing the literature sweep to redirect the thesis.

## Execution Stages
1. Initialize status tracking and inspect existing artifacts from attempt 2.
2. Build or reuse a literature corpus:
   - 1000-paper landscape sweep.
   - 300-paper serious skim from metadata/abstracts.
   - 200-250-paper deeper read from abstracts, available PDFs, and closest-paper metadata.
   - 100-paper hostile prior-work set.
3. Generate required literature artifacts:
   - `docs/related_work_matrix.csv`
   - `docs/literature_map.md`
   - `docs/hostile_prior_work.md`
   - `docs/novelty_boundary_map.md`
   - `docs/novelty_decision.md`
   - `docs/claims.md`
   - `docs/reviewer_attacks.md`
4. Choose the strongest thesis only after mapping hidden assumptions and hostile prior work.
5. Build runnable evidence with a small reproducible embodied-manipulation/perception experiment.
6. Write an anonymous ICLR-style paper using the latest official template available at runtime.
7. Compile the paper and save the final PDF to `C:/Users/wangz/Downloads/29.pdf`.
8. Create or update the public GitHub repo `29_gripper_dependent_object_identity` and push the complete runnable repo, documenting any failure.
9. Write `docs/final_audit.md` with the required 13 audit answers.

## Safety Notes
- Use noninteractive, bounded commands with explicit timeouts for long work.
- Avoid fragile inline PowerShell/Python for complex parsing; create scripts instead.
- Preserve useful prior artifacts if present.
- Keep claims conservative and mark unsupported claims clearly.
