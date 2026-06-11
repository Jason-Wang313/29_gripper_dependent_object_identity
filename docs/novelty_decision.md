# Novelty Decision

## Decision
Proceed with the thesis: **object identity for robot manipulation should be represented as an interface-conditioned partition, not as a single gripper-agnostic label, whenever different gripper-action channels induce non-nested observability relations.**

## New Central Mechanism
The central mechanism is the **Interface-Conditioned Identity Partition (ICIP)**. For a gripper-action family `g`, ICIP defines two latent object states as the same identity when their observation distributions and task-relevant manipulation outcomes are indistinguishable under `g`. The identity relation is therefore indexed by the gripper-action interface.

## Why This Beats The Alternatives
- Compared with bigger models, ICIP changes the target variable.
- Compared with active perception, ICIP changes what identity means after an action channel is selected.
- Compared with affordances, ICIP separates "what action is possible" from "which object distinctions are observable and sufficient for this interface."
- Compared with a benchmark, ICIP gives a formal failure condition: non-nested partitions prevent a single identity from being both observable and sufficient.

## Evidence Required
The paper needs: a finite-partition proposition, a runnable synthetic manipulation-perception environment with multiple grippers, collision/non-nesting metrics, and planner/classifier comparisons showing that global object IDs and common gripper-agnostic labels fail in different ways.
