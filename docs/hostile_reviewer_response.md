# Hostile Reviewer Response

## Likely Rejection

The work is a tidy partition argument in a toy world. Real systems can use richer sensors, active probing, or a universal latent state; ICIP also fails if the task needs a property the gripper cannot observe.

## Honest Response

We agree. ICIP is not a replacement for sensing or active information gathering. It says the deployable identity label should be the quotient induced by what an interface can observe and what the task needs.

The v2 stress quantifies the failure boundary. When pinch must condition on porosity, suction on friction, and enveloping on mass, each gripper lacks the needed observation channel and ICIP action success falls from 100.0% to 50.0%. The paper should claim ICIP only when the interface observes the task-relevant quotient or can abstain/request more sensing.

## Required Upgrade For Main-Track Submission

- Evaluate on a real multi-gripper manipulation dataset.
- Measure actual observation partitions from tactile/force/vision traces.
- Add active sensing or abstention when the task partition is not observable.
- Compare against universal latent-state, multimodal fusion, and affordance-conditioned baselines.
