# Abstraction boundaries

What each mechanism in the codebase stands for, and — more importantly — what
it does not.

Neural Accord does **not** claim that a symbolic channel is a literal synapse,
that it simulates an entire brain, or that it establishes a theory of
consciousness.

## Constraint map

| Feature | Biological target | Status | Limitation |
|---|---|---|---|
| Discrete event transmission | Quantal neurotransmitter release | `ABSTRACTED` | A token is not a vesicle; a synapse is not a network socket |
| Probabilistic omission | Release failure / unreliable effective transmission | `ABSTRACTED → MODELLED` | Fixed erasure is Level 0 only; later models use state-dependent release |
| Bounded signaling window | Temporal, metabolic, and refractory constraints | `ABSTRACTED` | Neural models use time, spike, and activity budgets rather than message length |
| Facilitation/depression | Activity-history-dependent efficacy | `MODELLED` | Parameters are specific to a named evidence profile and conditions |
| Local plasticity | Activity-dependent synaptic change | `MODELLED / HYPOTHESIS` | No rule is treated as a complete theory of learning or memory |
| SILENCE | Observable erasure for diagnostic control | `ABSTRACTED` | Postsynaptic systems do not receive a labeled notice of a failed release |
| Substitution | Effective interference / decoding ambiguity | `ABSTRACTED` | Neural models use competing activity, timing jitter, and background noise |
| Decoder drift | Changing neural/recording/strategy relationship across sessions | `MEASURED / MODELLED` | BCI implementation requires task-specific real-data validation |

## Why SILENCE and substitution stay separate

`core.channels.base.Outcome` distinguishes `SILENCE` from `SUBSTITUTED`
because erasure and interference are different problems for a coordinating
system, and a trace that merges them cannot tell them apart afterwards.
`SILENCE` is explicitly a **diagnostic control**: a labeled notice of failure
is a research instrument, not a biological claim. Level 2 and above remove the
label and force the system to infer failure from activity.

## Evidence labels

| Label | Meaning |
|---|---|
| `MEASURED` | Direct observation in a named species, circuit, connection class, and condition |
| `MODELLED` | Published model fitted to or constrained by empirical data |
| `ABSTRACTED` | Deliberate simplification with documented retained and omitted properties |
| `HYPOTHESIS` | Untested project prediction; never represented as settled fact |

Describing an abstraction as a biological measurement is the error this
document exists to make hard to commit.
