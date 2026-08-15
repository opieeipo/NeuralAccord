# Related work and novelty audit

A scan of prior art against this project's claims, run 2026-08-15. It exists to
stop the platform re-deriving results that already exist, and to say plainly
which of its hypotheses are still unclaimed.

Findings carry the project's own evidence labels, applied here to *claims about
the literature* rather than about biology:

| Label | Meaning in this document |
|---|---|
| `MEASURED` | Read the source and confirmed directly |
| `MODELLED` | Inferred from abstracts, indexes, and search summaries |
| `HYPOTHESIS` | A gap that appears to exist but that absence of evidence does not establish |

**This audit is not exhaustive.** It was a targeted scan, not a systematic
review. A negative result here means "not found", which is weaker than "does not
exist" — the same standard the project applies to its own unknowns.

---

## 1. Level 0 is replication, and should be labelled as such

`MEASURED`

Convention formation in a Lewis signalling game under an unreliable channel is
well covered. Most directly, [Vital et al. (2025)](https://arxiv.org/abs/2502.12624)
extend the Lewis signalling game with channel and input noise and report that
agents **add redundancy to transmitted messages** to offset it — which is the
same effect this project's H1 predicts and which the Level 0 demo reproduces at
signalling budget 2.

Related: [Nikolaus et al. (2024)](https://openreview.net/forum?id=Sy8upuD6Bw) on
conversational repair, and [Kuciński et al. (2021)](https://arxiv.org/abs/2111.06464),
who report that a noisy channel is itself sufficient to induce compositional
communication.

**Consequence.** Level 0 has no claim to novelty and should be presented as the
project's blank-slate **control condition** — the baseline that any effect
attributed to richer structure must be measured against. It is not a
contribution and the demo page now says so.

**Consequence for H1.** As currently stated, H1 is close to an already-published
result. To remain a live hypothesis it needs the part that is not yet done: the
comparison against *state-dependent* transmission drawn from a named evidence
profile, rather than fixed noise.

---

## 2. Constrained interfaces between pretrained systems — active, but with a specific hole

`MEASURED`

The redesign direction — two representation-rich systems communicating through a
constrained interface — is an active area, so it cannot be entered naively.

The nearest neighbour is
[*Latent Communication Between Language Model Agents* (2026)](https://arxiv.org/html/2607.14103),
which compares dense 4096-dimensional residual-stream vectors, SAE-sparse codes
at 28× compression, and plain text as channels between Llama and Mistral. It
confirms representational convergence across independently pretrained models
(92% retrieval accuracy) and finds text outperforms latent channels on tasks that
are fully text-expressible.

Read directly, that paper explicitly does **not**:

- model channel noise, dropout, bandwidth limits, or any unreliability — its
  only information loss comes from representation conversion;
- use any biological constraint;
- study how a protocol *develops*, examining final trained states only.

Also in this space:
[*Neural Communication Systems with Bandwidth-limited Channel*](https://arxiv.org/abs/2003.13367)
and emergent-communication fine-tuning of pretrained language models.

**Consequence.** The interface-between-rich-systems framing is not open ground on
its own. What remains open is the intersection with unreliability, biological
constraint, and development — which is precisely where this project already
intended to sit.

---

## 3. The biological side is mature, and separate

`MEASURED`

Stochastic vesicle release and short-term plasticity as constraints on
information transfer is established computational neuroscience — including
[Rotman et al. (2011)](https://www.jneurosci.org/content/31/41/14800), already
cited in this repository, and work showing that stochastic release suppresses
low-frequency information relative to high, and that short-term plasticity can
either raise or lower information transfer depending on input statistics.

This literature concerns transfer **at a synapse between neurons**. It is not
about coordination between two systems that already have rich internal
representations.

---

## 4. The intersection appears to be the gap

`HYPOTHESIS`

Searching specifically for biologically-constrained synaptic interfaces between
artificial agents — quantal release, facilitation and depression, measured
species profiles, applied as the channel between representation-rich systems —
returned nothing integrating these elements.

Each ingredient is mature in isolation. The combination is where this project's
distinctive position lies, and it is also what the current implementation does
not yet do: the Level 0 channel is a serial token socket between two systems
with no representations at all.

**This is a "not found", not a "does not exist".** Treat it as a direction worth
pursuing, not as an established claim of priority.

---

## 5. H4 — developmental archaeology — appears to be the strongest open claim

`MODELLED`

The adjacent area is active. Work exists on recovering training history from
model weights, including
[*Approximating Language Model Training Data from Weights*](https://arxiv.org/html/2506.15553),
[*Unsupervised Model Tree Heritage Recovery*](https://arxiv.org/pdf/2405.18432),
and weight-space analysis that recovers checkpoint ordering along training
trajectories. [Developmental interpretability](https://devinterp.com/) studies
the emergence of internal structure through training phase transitions using
singular learning theory.

All of this asks a **capability** question: *can X be recovered from weights?*

H4 asks something structurally different — a **dissociation**: whether a system
can retain full functional competence while its developmental route becomes more
recoverable from a complete external trace than from its own current operative
state. The Husserlian framing of sedimentation did not appear anywhere in this
space.

Supporting signal: the nearest latent-communication work above examines final
trained states only and does not investigate protocol development at all, which
leaves the developmental axis conspicuously unoccupied in that literature.

**Consequence.** H4 is the most defensible novelty in the project and is
currently the least built. That ordering should probably be reversed.

---

## 6. H6 — calibration burden — is substantially claimed

`MEASURED`

This is the most significant negative finding, and it affects a track the README
treats as a headline contribution.

The [FALCON benchmark](https://openreview.net/forum?id=FN02v4nD8y) (NeurIPS 2024,
Datasets and Benchmarks) already standardises evaluation of intracortical BCI
decoders under exactly the conditions the README describes: held-in sessions with
enough data to train a decoder, **held-out sessions with deliberately
insufficient data**, few-shot evaluation, multi-unit threshold crossings, human
and primate motor and communication tasks, and an explicit goal of stable
decoding over weeks with minimal new-day data.

Alongside it: an [MS-ITR metric](https://pmc.ncbi.nlm.nih.gov/articles/PMC9954620/)
that scores performance *and* the calibration data required, on the explicit
argument that accuracy alone ignores the information cost of achieving it — which
is the README's argument; and [EDAPT](https://iopscience.iop.org/article/10.1088/1741-2552/ae5689)
on calibration-free BCI via continual online adaptation.

**Consequences.**

1. "Calibration burden rather than offline accuracy" is not a novel reframe. It
   is an existing and increasingly standard position.
2. FALCON is directly relevant prior art that this repository does not cite. It
   should be in `references.bib` and in the baseline registry discussion
   regardless of what else changes.
3. H6 needs restating. A defensible remaining version is narrower: whether
   *biologically motivated* stability and uncertainty mechanisms lower burden
   against FALCON-style baselines — a question about mechanism, not about the
   metric.

---

## What this implies for sequencing

- **Level 0** — keep, relabelled as the control condition. Done.
- **H1** — needs the dynamic-synapse comparison to stay distinct from Vital et al.
- **H6** — benchmark against FALCON rather than proposing a parallel framework;
  narrow the claim to mechanism.
- **H4** — the strongest open claim, and the least built.
- **The interface redesign** — enters an active field, so it needs the biological
  constraint and the developmental trace to be more than a re-entry.

## Maintaining this document

Re-run before any claim of novelty appears in a paper, a grant application, or
the README. Record the date and what was searched. An audit with no date is not
evidence.
