# Literature Map

## Corpus
- Landscape sweep: 1000 rows in `docs/related_work_matrix.csv`.
- Serious skim: 300 highest-scored rows in `data/serious_skim_300.csv`.
- Deep read: 225 highest-scored rows in `data/deep_read_225.csv`.
- Hostile set: 100 closest rows in `data/hostile_prior_work_100.csv` and expanded in `docs/hostile_prior_work.md`.
- Retrieval source: Crossref metadata/abstracts because OpenAlex and Semantic Scholar returned HTTP 429 during this attempt. This is enough for a broad map, but it is not a substitute for a final human full-PDF literature review.

## Field Box
The relevant field box is manipulation perception for embodied agents: tactile and visuotactile object recognition, active/interactive perception, gripper hardware that changes sensing, object-centric manipulation representations, affordance learning, and task-conditioned manipulation planning.

The strongest boundary question is not whether touch improves object recognition. The stronger question is whether "object identity" itself should be indexed by the robot interface when the gripper-action channel changes what can be observed and what distinctions matter for control.

## Time Distribution
{
  "2020-2026": 570,
  "2000-2009": 66,
  "2010-2019": 331,
  "pre-2000": 33
}

## Mechanism Clusters
{
  "active perception policy": 511,
  "tactile/visuotactile representation": 271,
  "grasp synthesis or grasp quality model": 240,
  "pose/category-level perception": 200,
  "robot learning control policy": 128,
  "deformable/contact dynamics model": 106,
  "object-centric latent world model": 49,
  "robotics perception/manipulation method": 43,
  "affordance learning model": 35,
  "sim-to-real or domain adaptation": 13,
  "soft/suction gripper mechanism": 10,
  "planner using object/task representation": 3,
  "object recognition representation": 2
}

## High-Pressure Papers
- 1. Perception, control, and hardware for in-hand slip-aware object manipulation with parallel grippers (2025, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 2. Systematic object-invariant in-hand manipulation via reconfigurable underactuation: Introducing the RUTH gripper (2021, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 3. Bioinspired Swallowing Soft Gripper with Toroidal Optical Waveguides for Multimodal Interactive Perception (2026, Soft Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 4. Enhancing user perception through haptic feedback during aerial manipulation (2026, Industrial Robot: the international journal of robotics research and application): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 5. Teaching and Reproduction for In-Hand Object Manipulation (2025, Journal of Robotics and Mechatronics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 6. Evaluation of different robotic grippers for simultaneous multi-object grasping (2024, Frontiers in Robotics and AI): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 7. Contact Location Display for Haptic Perception of Curvature and Object Motion (2005, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 8. Hand-object configuration estimation using particle filters for dexterous in-hand manipulation (2020, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 9. Towards automating construction tasks: Largescale object mapping, segmentation, and manipulation (2021, Journal of Field Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 10. Proprioceptive Object Shape and Size Extraction via In-Hand-Manipulation with a Variable Friction Robot Gripper (2025, 2025 IEEE International Conference on Robotics and Automation (ICRA)): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 11. Shared visuo-tactile interactive perception for robust object pose estimation (2025, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 12. Object recognition using tactile sensing in a robotic gripper (2022, Insight - Non-Destructive Testing and Condition Monitoring): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 13. Perception, navigation, and manipulation in the team KAUST approach to the MBZIRC ground robotics challenge (2019, Journal of Field Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 14. Robotic Perception and Manipulation in Unstructured Environments (2025, International Journal on Mechanical Engineering and Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 15. A Novel Reconfigurable Modular Gripper for In-Hand Object Manipulation and Release With Appropriate Posture (2016, Volume 5A: 40th Mechanisms and Robotics Conference): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 16. Effect of Cutaneous Feedback on the Perception of Virtual Object Weight during Manipulation (2020, Scientific Reports): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 17. Robotic perception and manipulation of deformable linear objects: A survey (2026, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 18. Leveraging depth data in remote robot teleoperation interfaces for general object manipulation (2020, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 19. Gripper Pose and Object Pointflow as Interfaces for Robotic Bimanual Manipulation (2025, Robotics: Science and Systems XXI): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 20. Human Perception of Inertial Mass for Joint Human-Robot Object Manipulation (2018, ACM Transactions on Applied Perception): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels

## Hostile Center of Mass
- 2. Systematic object-invariant in-hand manipulation via reconfigurable underactuation: Introducing the RUTH gripper (2021, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 4. Enhancing user perception through haptic feedback during aerial manipulation (2026, Industrial Robot: the international journal of robotics research and application): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 3. Bioinspired Swallowing Soft Gripper with Toroidal Optical Waveguides for Multimodal Interactive Perception (2026, Soft Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 1. Perception, control, and hardware for in-hand slip-aware object manipulation with parallel grippers (2025, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 7. Contact Location Display for Haptic Perception of Curvature and Object Motion (2005, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 8. Hand-object configuration estimation using particle filters for dexterous in-hand manipulation (2020, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 5. Teaching and Reproduction for In-Hand Object Manipulation (2025, Journal of Robotics and Mechatronics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 12. Object recognition using tactile sensing in a robotic gripper (2022, Insight - Non-Destructive Testing and Condition Monitoring): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 6. Evaluation of different robotic grippers for simultaneous multi-object grasping (2024, Frontiers in Robotics and AI): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 13. Perception, navigation, and manipulation in the team KAUST approach to the MBZIRC ground robotics challenge (2019, Journal of Field Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 16. Effect of Cutaneous Feedback on the Perception of Virtual Object Weight during Manipulation (2020, Scientific Reports): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 9. Towards automating construction tasks: Largescale object mapping, segmentation, and manipulation (2021, Journal of Field Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 15. A Novel Reconfigurable Modular Gripper for In-Hand Object Manipulation and Release With Appropriate Posture (2016, Volume 5A: 40th Mechanisms and Robotics Conference): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 14. Robotic Perception and Manipulation in Unstructured Environments (2025, International Journal on Mechanical Engineering and Robotics): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 22. Using 3D Convolutional Neural Networks for Tactile Object Recognition with Robotic Palpation (2019, Sensors): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 17. Robotic perception and manipulation of deformable linear objects: A survey (2026, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 11. Shared visuo-tactile interactive perception for robust object pose estimation (2025, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labe...
- 10. Proprioceptive Object Shape and Size Extraction via In-Hand-Manipulation with a Variable Friction Robot Gripper (2025, 2025 IEEE International Conference on Robotics and Automation (ICRA)): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 23. Leveraging Human Perception in Robot Grasping and Manipulation Through Crowdsourcing and Gamification (2021, Frontiers in Robotics and AI): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels
- 18. Leveraging depth data in remote robot teleoperation interfaces for general object manipulation (2020, The International Journal of Robotics Research): formal equivalence classes induced by gripper-action observation channels; morphology-indexed object identity rather than embodiment-invariant labels

## Hidden Assumptions That May Be False
1. Object identity is independent of the robot hand or end-effector.
2. The sensor stream is a sufficient statistic for object identity regardless of action.
3. A category label is stable across changes in contact geometry.
4. Visual appearance dominates contact-mediated evidence.
5. The gripper can be treated as an interchangeable actuator, not part of perception.
6. Success/failure labels reveal object properties without morphology confounds.
7. Object shape can be inferred without specifying the probe that generated observations.
8. Training and deployment grippers induce comparable observation channels.
9. A single latent object embedding can serve all manipulation actions.
10. Tactile readings are sensor features rather than gripper-object relational events.
11. Affordances are properties of objects alone rather than object-gripper-action triples.
12. A manipulation policy can reuse object IDs across tools without recalibration.
13. Object mass, friction, compliance, and geometry are separable from the grasp family.
14. Benchmark labels correspond to the distinctions a deployed gripper can observe.
15. In-hand observations are exchangeable across finger layouts and contact patches.
16. Sim-to-real gaps mainly concern physics parameters, not identity partitions.
17. Active perception chooses actions but assumes the object identity target is fixed.
18. The object model need not represent unobservable equivalence classes.
19. Multi-modal fusion improves identity without modeling which modality is action-gated.
20. Planning can consume object labels without knowing their gripper-conditioned validity.
21. A learned representation that is invariant across embodiments is always beneficial.
22. The same failure mode has the same semantic meaning for suction, pinch, and enveloping hands.
23. Contact observables reveal intrinsic object state rather than a quotient of state by probe.
24. Data augmentation over views substitutes for physical probing diversity.
25. Closed-loop manipulation can correct perception errors without redefining identity.

## Directions Considered
1. Bigger tactile recognition model: rejected because it keeps the object label fixed and only improves estimation.
2. Active probing for object classification: rejected as central contribution because active perception already chooses actions under a fixed target identity.
3. Multi-gripper benchmark: rejected as central contribution because a benchmark alone does not change the mechanism.
4. Affordance-only reframing: useful but insufficient because affordances can still assume object labels are stable and separate from the observing interface.
5. Interface-conditioned identity partitions: chosen because it changes the central variable from an embodiment-invariant object ID to the quotient of latent object states induced by a gripper-action observation channel.

## Chosen Direction
The paper should formalize and test interface-conditioned identity partitions. The core move is to treat each gripper-action family as inducing an observation-and-control equivalence relation over latent object states. A "same object" relation for manipulation is then not universal; it is indexed by the interface that produces the observables.
