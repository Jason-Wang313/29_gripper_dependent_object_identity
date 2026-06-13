# Experiment Rigor Checklist

- [x] Main synthetic experiment is `experiments/run_icip_experiment.py`.
- [x] Main world has 96 latent objects and three gripper interfaces.
- [x] Baselines include global ID, common gripper-agnostic label, and ICIP.
- [x] Metrics include label accuracy, action success, global-ID ceiling, and partition relations.
- [x] V2 hidden-task stress attacks the assumption that the interface observes task-relevant attributes.
- [x] Negative boundary is explicit: ICIP drops from 100.0% to 50.0% when the task requires a gripper-hidden attribute.
- [ ] No real robot validation.
- [ ] No high-fidelity tactile or force simulator.
- [ ] No learned observation partition.
- [ ] No active sensing or abstention policy.

Decision: mechanism evidence only; terminal state is workshop-only / strong-revise.
