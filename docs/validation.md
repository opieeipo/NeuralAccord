# Validation and the reproducibility contract

A result that does not carry all of the following is not reportable.

## Every result

- [ ] Versioned YAML **and** the fully resolved configuration.
- [ ] Seed list, seed-level outcomes, and variance — not a single best run.
- [ ] Exact software environment and dependency lockfile (`uv.lock`).
- [ ] Dataset manifests, checksums, transformations, and source citations.
- [ ] Declared biological omissions and unknown parameters.
- [ ] Complete or privacy-safe developmental trace, sufficient for independent
      analysis.
- [ ] Task controls: no communication, randomized communication, fully shared
      observations, and matched fixed/dynamic-noise conditions where
      applicable.

## Biological profiles additionally

- [ ] Species, region, layer, cell/connection class, parameter source, and
      uncertainty for every parameter used.
- [ ] Biological validation error against each declared target, reported per
      target rather than aggregated.
- [ ] The fidelity level, and a conclusion that does not exceed it.

## BCI profiles additionally

- [ ] Dataset access restrictions and the governing agreement.
- [ ] Preprocessing decisions, in order.
- [ ] Strictly chronological split — no random intermixing of future and
      historical trials.
- [ ] Label budget and baseline versions.
- [ ] Performance versus current-session label budget (the curve, not a point).
- [ ] Area under the calibration curve.
- [ ] Zero-shot performance using historical sessions only.
- [ ] Recovery burden after drift, channel loss, or feature degradation.
- [ ] Retention cost: whether adapting to a new session damages prior-session
      performance.
- [ ] Closed-loop task metrics where feasible: target acquisition, throughput,
      path efficiency, success rate, time-to-target.
- [ ] Online adaptation and inference latency.
- [ ] User-facing burden: prompted trials, calibration minutes, failures, and
      explicit recalibration events.

A method does **not** count as burden-reducing merely because it has a higher
final score after requiring more calibration.

## Controls that are not optional

The chance baseline is declared before the run, not fitted afterwards.
Reward-leakage controls accompany every Level 0 result. Cross-play between
independently trained systems is reported alongside self-play, because
self-play scores alone do not establish that a convention is shared rather
than idiosyncratic.

## Negative results

Collapse regimes are reported with the same care as success regimes. A sweep
that finds only failure is a result; a sweep whose failing arm is unreported is
a defect.
