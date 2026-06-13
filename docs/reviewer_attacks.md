# Reviewer Attacks

1. **This is just affordances.** Response: affordances model action possibilities; ICIP models the identity relation induced by observability and task sufficiency for a gripper-action channel. The same affordance can still leave identity over-refined or under-refined.
2. **This is just active perception.** Response: active perception selects informative actions for a fixed latent target. ICIP asks whether the target identity relation itself changes when the action/gripper channel changes.
3. **The experiment is synthetic.** Concede. The paper should be judged as a formal/mechanistic position with runnable evidence, not as a real-robot systems paper.
4. **A universal latent state can contain all attributes.** Response: a full latent state may exist, but a gripper cannot necessarily observe it. The claim concerns deployable identity labels that are both observable and sufficient.
5. **A downstream planner could ignore irrelevant global-label distinctions.** Response: yes, and that is exactly the quotient argument; if distinctions are irrelevant/unobservable for the interface, the identity abstraction should quotient them out.
6. **Multi-modal models can fuse vision and touch.** Response: fusion still needs to model which distinctions each action-gated modality can reveal.
7. **The literature search is noisy.** Concede. Crossref produced broad coverage under rate limits; hostile papers were inspected at metadata/abstract level, and final submission would require manual full-PDF verification.
8. **No real robot.** Concede. Paper-readiness should be workshop/revise unless paired with real robot validation.
9. **The theorem is obvious.** Response: the novelty is not lattice theory alone; it is applying the observability/sufficiency conflict to object identity in gripper-dependent manipulation perception and making it operational.
10. **The name identity may confuse readers.** Response: define it operationally as a task-facing equivalence relation, not metaphysical object sameness.
11. **ICIP fails if the gripper cannot sense a task-critical property.** Response: yes, and v2 quantifies it. When tasks require porosity for pinch, friction for suction, or mass for enveloping, ICIP action success falls from 100.0% to 50.0%. The claim is conditional on the interface observing the task-relevant quotient or on adding sensing/abstention.
