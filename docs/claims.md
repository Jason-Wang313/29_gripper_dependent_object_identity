# Claims

## Supported Claims
1. In finite latent-state manipulation settings, every gripper-action observation channel induces an equivalence relation over object states.
2. If two grippers induce non-nested partitions and their task outcomes require their respective distinctions, no single gripper-agnostic identity partition can be both observable for each gripper and sufficient for each gripper's task.
3. The synthetic experiment demonstrates this failure mode for pinch, suction, and enveloping grippers: global IDs are not observable from a single gripper's channel, while the common gripper-agnostic label is observable but loses task-relevant distinctions.
4. Interface-conditioned identity partitions recover the observable and task-sufficient distinctions in the toy environment.
5. The v2 hidden-task stress shows the boundary: if the task requires an attribute hidden from the interface, ICIP action success drops from 100.0% to 50.0% for pinch, suction, and enveloping.

## Unsupported Or Only Partially Supported Claims
1. The paper does not prove the phenomenon dominates real robot datasets.
2. The paper does not introduce a new tactile sensor, gripper, or physical robot benchmark.
3. The paper does not show real-world robot trials.
4. The literature sweep is broad metadata/abstract coverage, not a verified full-PDF review of all 1000 entries.
5. The paper does not solve missing sensing; hidden task-relevant attributes require another sensor, another interface, information gathering, or abstention.

## Formal-Claim Status
The main theorem is a finite partition impossibility result. It is proof-level in the paper if assumptions are stated exactly. The experiment is illustrative evidence, not a real-robot validation.
