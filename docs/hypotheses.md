# Hypotheses

Each hypothesis is stated so it can fail. A hypothesis with no declared
falsifying outcome is not ready to be listed here.

## H1 — Dynamic reliability

Under some task regimes, state-dependent transmission and limited signaling
capacity favor distributed, robust, or redundant coordination relative to a
matched fixed-noise baseline.

- **Falsified if:** across the declared seed list, dynamic-synapse conditions
  show no regime where coordination robustness exceeds the matched fixed-noise
  control beyond seed-level variance.
- **Requires:** Level 1, matched fixed/dynamic-noise controls.

## H2 — Boundary sensitivity

At intermediate private-observation rates, systems develop behavior associated
with common-ground boundaries rather than merely ignoring private observations.

- **Falsified if:** behavior at intermediate rates is indistinguishable from a
  policy that discards private observations outright.
- **Requires:** private-observation rate sweep, fully-shared-observation
  control.

## H3 — Maintenance

Persistent competence depends on more than static weights; recurrent dynamics,
short-term synaptic state, homeostasis, replay, and structural reorganization
make separable contributions.

- **Falsified if:** ablating each mechanism in turn leaves competence
  unchanged, or the contributions prove inseparable under the declared
  protocol.
- **Requires:** Level 2+, perturbation and recovery protocols.

## H4 — Retention dissociation

A mature system can preserve useful coordination while its developmental route
is more recoverable from a complete external trace than from current operative
state.

- **Falsified if:** lineage recovery from current state matches recovery from
  the complete trace.
- **Requires:** complete developmental trace, explicit-memory controls.

## H5 — Cross-species transfer

Some effects survive mouse/human profile differences; others are sensitive to
species-specific parameters or network architecture.

- **Falsified if:** every measured effect is invariant across profiles, or the
  human profile has too many `unknown` parameters to support a comparison —
  the second outcome is a reportable negative result about evidence
  availability, not about biology.
- **Requires:** populated mouse and human profiles, comparative profile.

## H6 — Calibration reduction

Under chronological cross-session evaluation, an uncertainty-aware co-adaptive
method can reach a predeclared control threshold with fewer current-session
labels, less prompted time, or faster recovery after drift or channel loss
than declared baselines.

- **Falsified if:** B_tau for the co-adaptive method is not below the declared
  baselines' on permitted real data under the same split, preprocessing, and
  reporting pipeline.
- **Requires:** Level 4, permitted dataset, task-specific baseline registry.
- **Note:** a higher final score after *more* calibration does not count.
