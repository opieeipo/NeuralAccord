# Neural Accord

An open research platform for investigating how adaptive coordination develops,
persists, and becomes historically opaque under biologically motivated neural
constraints.

The project overview, research questions, fidelity ladder, and BCI
co-adaptation track live in the [repository README](https://github.com/opieeipo/NeuralAccord#readme).
These pages hold the working documents that a contribution has to satisfy:

- **[Provenance](provenance.md)** — what has to travel with a biological value,
  and why there is no mammalian default.
- **[Biological constraints](biological-constraints.md)** — the mouse, human,
  and comparative profiles, and what each fidelity level permits you to
  conclude.
- **[Abstraction boundaries](abstraction-boundaries.md)** — what each mechanism
  stands for, and what it does not.
- **[Hypotheses](hypotheses.md)** — H1–H6, each with its falsifying outcome.
- **[Validation](validation.md)** — the reproducibility contract, as a
  checklist.
- **[Related work](related-work.md)** — a dated novelty audit: what is already
  claimed in the literature, and which hypotheses remain open.

## Interactive pages

- **[Synaptic Emergence — Level 0](demo/synaptic-emergence.html)** — the project's
  blank-slate **control condition**, run live: two systems with no prior
  representation of the world forming a convention through a channel that erases
  and corrupts, alongside the no-communication and randomized-communication
  controls. It reproduces a known result on purpose; see
  [Related work](related-work.md).
- **[The fidelity ladder](demo/fidelity-ladder.html)** — what each level lets you
  conclude, the four evidence labels, and where each mechanism stops being a
  biological claim.
- **[Calibration burden](demo/calibration-burden.html)** — why B<sub>τ</sub>
  rather than offline accuracy is the unit of claim in the BCI track, with a
  threshold slider that inverts which method wins.

Sources and the build step are described in
[`docs/demo/README.md`](https://github.com/opieeipo/NeuralAccord/blob/main/docs/demo/README.md)
in the repository.

## Status

Specification and research invitation. The first deliverable is a tested,
reproducible Level 0 baseline, versioned mouse/human evidence profiles, and BCI
benchmark interfaces that make calibration-burden claims falsifiable.
