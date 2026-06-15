# Experiment Rigor Checklist

- [x] Legacy audit experiment is `experiments/run_icip_experiment.py`.
- [x] Full-scale v3 experiment is `experiments/full_scale_icip_experiment.py`.
- [x] Full-scale world has 373,248 latent states.
- [x] Full-scale suite has 7 interfaces and 6 regimes.
- [x] Baselines include global ID, common label, oracle ICIP, learned ICIP, universal refinement, universal coarsening, multimodal fusion, interface routing, active ICIP, and abstaining ICIP.
- [x] Metrics include action success, label accuracy estimate, utility, coverage, abstention, observability violation, sufficiency gap, class count, false merge, and false split.
- [x] Hidden-task stresses attack the assumption that the interface observes task-relevant attributes.
- [x] Negative controls include aligned control, irrelevant-hidden control, and global-observable control.
- [x] Learned partition recovery is included under repeated noisy probes.
- [x] Active sensing, interface routing, multimodal fusion, and abstention are included.
- [x] Non-nesting prevalence sweep is included over random finite attribute worlds.
- [x] Cross-interface transfer matrix is included.
- [x] RAM-light strategy uses exact aggregate formulas and compact CSV outputs rather than raw traces.
- [ ] No real robot validation.
- [ ] No high-fidelity tactile or force simulator.

Decision: submission-ready as a formal/synthetic mechanism paper with explicit no-real-robot and no-prevalence boundaries.
