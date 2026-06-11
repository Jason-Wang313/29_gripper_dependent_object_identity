# Novelty Boundary Map

## What Prior Work Already Covers
- Tactile and visuotactile recognition: recognizing objects or properties from contact streams is well covered.
- Active and interactive perception: choosing actions to reveal state under partial observability is well covered.
- Grasp success prediction and gripper design: gripper morphology, suction, soft grippers, and in-hand mechanisms are well covered.
- Affordance learning: object-action possibility representations are well covered.
- Object-centric latent world models: learned object representations for planning are well covered.

## What The Chosen Paper Must Not Claim
- It must not claim the first tactile object recognition method.
- It must not claim the first active perception method.
- It must not claim gripper morphology has never mattered.
- It must not claim a new benchmark is itself the contribution.
- It must not claim that uncertainty, active learning, or a verifier solves the problem.

## Boundary Where Novelty Remains
The unclaimed boundary is a representational one: define identity as an interface-conditioned quotient of latent object states, then prove that non-nested gripper-induced partitions make a single embodiment-invariant identity either unobservable for some gripper or insufficient for some manipulation outcome.

## Closest Hostile Families
1. Interactive perception papers: close because they make action part of perception, but they typically keep the target object variable fixed.
2. Tactile object recognition papers: close because they use touch to classify, but the classes are treated as object-intrinsic.
3. Gripper hardware/perception papers: close because they expose morphology-specific observables, but they usually optimize the sensor or controller rather than redefining identity.
4. Affordance papers: close because they bind action and object, but they often model action possibilities rather than observation-channel equivalence classes.
5. Object-centric manipulation/world-model papers: close because they learn object variables, but they usually prefer invariance across embodiments.
