# Paper 29 Full-Scale Execution Plan

## Current State

- Paper: `29_gripper_dependent_object_identity`
- Thesis: object identity for robot manipulation should be an interface-conditioned partition, not a single gripper-agnostic label, whenever gripper-action channels induce different observability and task-sufficiency relations.
- Current manuscript: compact v2 argument with a 96-object toy world, three grippers, one finite partition proposition, a hidden-task stress, and a metadata-limited literature audit.
- Current strongest result: global object IDs are task-sufficient but not observable; common labels are observable but insufficient; ICIP is both observable and sufficient in the constructed baseline.
- Current biggest weakness: the evidence is hand-specified, small, and too favorable to ICIP; there is no empirical partition estimation, no broad noise/sensor-cost study, no active sensing or abstention, no universal latent-state baseline, no transfer test, and no high-coverage sensitivity analysis.

## Target Standard

The final paper must be a genuine full-scale manuscript, not a padded expansion. The final PDF must be at least 25 pages and must earn its length through:

- Larger finite worlds and many evaluated cases.
- Stronger baselines that try to rescue fixed object identity.
- Learned or empirical partition estimation rather than only oracle quotients.
- Noise, missing-modality, and hidden-task stress tests.
- Active sensing, abstention, and cross-interface routing policies.
- Sensitivity analyses over observability, task coupling, sensor cost, and train/test mismatch.
- Figures/tables that explain the phase boundaries and failure modes.
- Reproducibility material that lets a reviewer rerun everything without special packages.

## Experiment Design

### World Scale

Build a new RAM-light standard-library experiment runner. It should stream counters rather than materialize large tensors.

Planned latent state space:

- Attributes: size, shape, stiffness, porosity, friction, mass, fragility, thermal tolerance, texture, liquid content.
- Nominal categories: mixed cardinalities for at least thousands of latent objects.
- Interfaces: pinch, suction, enveloping, spatula, magnetic, needle, clamp.
- Each interface has a visible attribute subset, a noisy observation kernel, an action family, a task partition, and a sensor-cost model.
- Multiple regimes vary the relation between observation and task partitions.

### Methods and Baselines

Evaluate at least these identity/control strategies:

- `global_id`: full latent object identity, task-sufficient but generally unobservable.
- `common_label`: gripper-agnostic visible/common object label.
- `oracle_icip`: true interface-conditioned quotient.
- `learned_icip`: partition estimated from noisy observation/action-equivalence samples.
- `universal_refinement`: single shared partition that keeps every distinction needed by any interface.
- `universal_coarsening`: single shared observable common partition.
- `multimodal_fusion`: fixed-label baseline with access to union observations after extra sensing.
- `interface_router`: chooses a sensing/manipulation interface before committing.
- `active_icip`: buys extra probes when expected value exceeds cost.
- `abstaining_icip`: refuses unobservable task demands instead of pretending identity is known.

### Main Evaluations

1. Large baseline separation:
   - Compare label accuracy, action success, observability violation, sufficiency violation, class count, and probe cost.
   - Show that oracle and learned ICIP keep task-relevant distinctions without forcing hidden global labels.

2. Empirical partition estimation:
   - Estimate blocks from noisy samples with increasing train probes.
   - Report adjusted pair agreement, split errors, merge errors, and downstream action success.
   - Include seed sweeps and confidence intervals.

3. Non-nesting prevalence:
   - Sweep random interface feature maps and task maps.
   - Measure how often interface partitions are identical, nested, or non-comparable.
   - Report the fraction of cases where a universal identity is impossible under observability and sufficiency constraints.

4. Hidden-task and missing-sensing stress:
   - Inject task-relevant hidden attributes per interface.
   - Compare naive ICIP, active ICIP, multimodal fusion, and abstention.
   - Report when active sensing helps and when abstention is the only honest answer.

5. Sensor-cost phase diagram:
   - Sweep hidden-attribute probability and extra-probe cost.
   - Identify regions where active ICIP, abstention, universal latent labels, or common labels win.

6. Cross-interface transfer:
   - Train identity partitions on one interface and deploy on another.
   - Show when transfer is valid for nested partitions and fails for non-nested partitions.

7. Negative controls:
   - Aligned world where all interfaces share the same task partition: universal identity should match ICIP.
   - Purely observable world where global ID is recoverable: ICIP should not claim magic advantage.
   - Irrelevant hidden attributes: ICIP should not overreact to attributes that do not affect control.

8. Robustness and sensitivity:
   - Observation noise sweep.
   - Number of train probes per state.
   - Interface count and latent attribute cardinality.
   - Task granularity and class imbalance.
   - Distribution shift between training and test latent mixtures.

## RAM-Light Execution Strategy

- Use only Python standard library unless an existing local dependency is already required.
- Use deterministic seeds and sequential sweeps.
- Store large-case outputs as CSV/JSON summaries, not raw per-sample traces.
- Use streaming counters for pairwise relations and action outcomes.
- Keep figure/table generation separate from experiment execution.
- Avoid multiprocessing unless absolutely necessary; if used, limit worker count explicitly.
- Write checkpoints per regime so a partial failure does not lose completed sweeps.

## Manuscript Rewrite Plan

The final manuscript should be rewritten around the expanded evidence, not merely append tables to v2.

Proposed structure:

1. Abstract with exact v3 scale, mechanisms, and negative boundaries.
2. Introduction explaining why fixed object identity fails before model capacity enters.
3. Related work split into active perception, tactile recognition, affordances, object-centric representations, gripper morphology, and abstention/sensing.
4. Formalism:
   - observation partitions;
   - task partitions;
   - observable-sufficient interval;
   - ICIP definition;
   - universal identity impossibility;
   - empirical partition estimation;
   - active sensing and abstention extensions.
5. Experimental setup:
   - latent worlds;
   - interfaces;
   - tasks;
   - noise models;
   - baselines;
   - metrics;
   - computational budget.
6. Main results:
   - large-scale separation;
   - learned ICIP vs oracle;
   - non-nesting prevalence;
   - hidden-task stress;
   - sensor-cost phase diagram;
   - transfer;
   - negative controls.
7. Failure analysis:
   - where ICIP fails;
   - when universal identity is fine;
   - when active sensing beats abstention;
   - when abstention is the correct policy.
8. Limitations and external validity:
   - no real robot claim;
   - synthetic worlds are evidence for mechanism and falsification boundaries;
   - what real multi-gripper dataset would be needed.
9. Reproducibility statement with exact commands and artifact paths.
10. Appendices:
   - proof details;
   - algorithm pseudocode;
   - full baseline definitions;
   - full tables;
   - sensitivity details.

## Figures and Tables

Required final artifacts:

- Main scale table with world size, regimes, evaluated decisions, seeds, interfaces, methods.
- Main performance table by method and regime.
- Learned partition table by train probes/noise.
- Non-nesting prevalence table.
- Hidden-task stress table.
- Sensor-cost phase diagram table or figure.
- Cross-interface transfer matrix.
- Negative-control table.
- Appendix sensitivity tables.
- At least 4 generated figures:
  - action success by method/regime;
  - learned partition recovery vs probes;
  - non-nesting prevalence;
  - active/abstention phase diagram.

## Documentation Updates

After experiments and manuscript finalization:

- Update `README.md` with v3 scale, exact results, build command, and final PDF hash.
- Update `child_status.md` with final state.
- Update `docs/final_audit.md`.
- Update `docs/claims.md`.
- Update `docs/experiment_rigor_checklist.md`.
- Update `docs/reproducibility_checklist.md`.
- Update `docs/submission_readiness_decision.md`.
- Update `docs/submission_version_log.md`.
- Update `docs/hostile_reviewer_response.md`, `docs/reviewer_attacks.md`, and `docs/submission_attack_log.md`.
- Add or update results README/validation JSON if useful.

## Final Acceptance Checklist

- Full-scale experiment runner completes from repo root on a normal machine.
- No uncontrolled RAM growth; outputs are summaries and compact tables.
- Results include strong baselines, negative controls, sensitivity sweeps, and failure cases.
- Paper explicitly avoids claiming real-robot validation.
- Manuscript compiles without undefined references/citations.
- Final PDF is at least 25 pages.
- Final PDF is copied only to `C:\Users\wangz\Downloads\29.pdf`.
- Local `paper/main.pdf` is removed after final export.
- PDF text contains v3 markers and scale numbers.
- Docs/logs/reproducibility files match the final results.
- Git worktree is clean after commit.
- Commit is pushed and local `HEAD` equals upstream.
