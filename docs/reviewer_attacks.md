# Reviewer Attacks

1. **This is just affordances.** Response: affordances model action possibilities; ICIP models the identity relation induced by observability and task sufficiency for a gripper-action channel.
2. **This is just active perception.** Response: active perception selects informative actions for a fixed latent target. ICIP asks whether the target identity relation itself changes when the action/gripper channel changes.
3. **The experiment is synthetic.** Concede. The paper should be judged as a formal/synthetic mechanism paper, not as a real-robot systems paper.
4. **A universal latent state can contain all attributes.** Response: a full latent state may exist, but a gripper cannot necessarily observe it. The claim concerns deployable identity labels that are both observable and sufficient.
5. **A downstream planner could ignore irrelevant global-label distinctions.** Response: yes, and that is exactly the quotient argument; if distinctions are irrelevant/unobservable for the interface, the identity abstraction should quotient them out.
6. **Multimodal models can fuse vision and touch.** Response: v3 includes multimodal fusion. It works when it changes the information state, but it has cost and does not erase the interface-conditioned quotient diagnosis.
7. **No learned partition.** Response: v3 includes exact learned partition recovery under noisy repeated categorical probes, including false-merge, false-split, and downstream action-success estimates.
8. **No active sensing or abstention.** Response: v3 includes active ICIP, interface routing, multimodal fusion, and abstaining ICIP.
9. **The literature search is noisy.** Concede. Crossref produced broad coverage under rate limits; many entries remain metadata/abstract-level and would need manual full-PDF verification for a literature-only claim.
10. **No real robot.** Concede. The paper is submit-ready only under the formal/synthetic mechanism framing.
11. **The theorem is obvious.** Response: the novelty is not lattice theory alone; it is applying the observability/sufficiency conflict to object identity in gripper-dependent manipulation perception and making it operational.
12. **The name identity may confuse readers.** Response: define it operationally as a task-facing equivalence relation, not metaphysical object sameness.
13. **ICIP fails if the gripper cannot sense a task-critical property.** Response: yes, and v3 makes that a central result. Hidden-pair tasks reduce naive/oracle ICIP to 10.7% action success; active sensing recovers only by acquiring the missing information.
14. **Universal identity works in some cases.** Response: yes. The aligned and global-observable negative controls show exactly when universal identity is appropriate.
