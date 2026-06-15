# Claims

## Supported Claims

1. In finite latent-state manipulation settings, every gripper-action observation channel induces an equivalence relation over object states.
2. An interface-conditioned identity partition is the minimal deployable quotient that is observable through an interface and sufficient for that interface's task partition.
3. If two interfaces induce distinct unique minimal observable-sufficient partitions, no single identity partition is the unique minimal identity for both.
4. If two required interface partitions are non-comparable, any single deployable compromise is either unobservable or insufficient for at least one interface.
5. The v3 full-scale suite demonstrates the mechanism over 373,248 latent states, 7 interfaces, 6 regimes, and 10 identity/control strategies.
6. In the baseline visible regime, oracle ICIP and learned ICIP reach 100.0% action success, while common gripper-agnostic labels reach 3.2%.
7. Hidden-task regimes show the boundary: hidden-pair tasks reduce naive/oracle ICIP to 10.7% action success.
8. Active sensing can restore success when targeted probes observe the missing task attributes; in the hidden-pair regime, active ICIP reaches 100.0% action success with 0.88 utility.
9. Negative controls show that universal identity is appropriate when all interfaces share the same task partition or when global state is observable.

## Unsupported Or Only Partially Supported Claims

1. The paper does not prove the phenomenon dominates real robot datasets.
2. The paper does not introduce a new tactile sensor, gripper, or physical robot benchmark.
3. The paper does not show real-world robot trials.
4. The literature sweep is broad metadata/abstract coverage, not a verified full-PDF review of all 1000 entries.
5. The simple active-sensing utility model is not a deployment-optimal safety policy.
6. ICIP does not recover hidden task variables without sensing, routing, task revision, or abstention.

## Formal-Claim Status

The main results are finite partition impossibility statements. The experiments are large synthetic mechanism evidence with negative controls and failure cases, not real-robot validation.
