# Critique: is Neural Accord aimed at the right thing?

**Status:** working document, drafted 2026-08-15 for external review.
**Not** a published page and not part of the documentation site.

This exists to be argued with. It records where the project's implementation
diverged from its intent, what a prior-art scan found, and what the author's
clarified end goal implies. A reviewer should be able to read it cold.

Evidence claims use the project's own labels, applied here to claims about the
literature rather than about biology:

| Label | Meaning here |
|---|---|
| `MEASURED` | Primary source read directly |
| `MODELLED` | Inferred from abstracts, indexes, search summaries |
| `HYPOTHESIS` | An apparent gap; absence of evidence, not evidence of absence |

Section 11 lists this document's own weaknesses. Read it before trusting the
rest.

---

## 1. The end goal, as clarified

The author's aim is **not** the aim the repository currently describes.

> Understand how signalling develops naturally in human grey matter, driven by a
> variety of signal structures rather than one modality — and then apply that
> architecture to machine learning, because the human brain performs comparable
> work at a small fraction of the power and processing cost of artificial neural
> networks.

The brain is the existence proof. The biology is a means. The intended output is
transferable architecture, not neurological understanding.

This differs from the nearest major effort in the field (§6). It also differs
from what this repository's README currently claims, which reads as a
neuroscience-understanding project. That mismatch is the root cause of the drift
described below.

---

## 2. What was actually built, and why it is off-target

A browser-based Lewis signalling game: two tabular-softmax agents learning a
symbol→meaning mapping through a channel with fixed erasure and substitution
rates, trained by a reward-modulated policy update, with no-communication and
randomized-communication controls, an analytically derived performance ceiling,
and deterministic seeding.

It is carefully built and verified. It is also the wrong object, for four
reasons.

**2.1 Meanings are integers with no geometry.** Meaning 3 bears no relation to
meaning 4. Any permutation of the symbol→meaning map is exactly as good as any
other, which is why the learned lexicon always resolves to an arbitrary
permutation matrix that changes with the seed. There is nothing to discover about
the world — only about the partner.

A direct consequence: the project's own README lists topographic similarity as a
core metric and requires "controls for the geometry of the input space." The
implementation has an input space with **no geometry at all**, making one of the
project's headline metrics undefined in its first deliverable.

**2.2 The interface is a serial token socket.** One symbol, occasionally two, per
episode. The README's constraint map explicitly warns "a synapse is not a network
socket." The implementation built a network socket.

**2.3 Nothing sits behind the interface.** Both parties are blank tables. The
author's stated design intent was an interchangeable intelligent backend — rich
representations on each side, with the interface as the constrained boundary. The
implementation has the constraint and no intelligence.

**2.4 It is not parallel.** A cortical neuron integrates on the order of 10³–10⁴
synapses across a spatially structured dendritic arbor with local nonlinear
integration. The model collapses this to a serial stream. This is not merely a
simplification; it removes the property most relevant to §7's efficiency thesis,
since parallel unreliable channels with local integration is where sparsity and
graceful degradation come from.

**Disposition.** Level 0 has been relabelled in the repository as the
**blank-slate control condition** — the baseline any claim about richer structure
must be measured against. It keeps its harness (seeding, controls, ceiling
analysis, chance baselines) and loses its billing.

---

## 3. Novelty audit of the original hypotheses

`MEASURED` unless noted. Full detail in `docs/related-work.md`.

| Claim | Status |
|---|---|
| **Level 0** — convention formation under an unreliable channel | **Replication.** [Vital et al. (2025)](https://arxiv.org/abs/2502.12624) extend the Lewis signalling game with channel noise and report agents adding redundancy to compensate — the same effect the demo reproduces. [Kuciński et al. (2021)](https://arxiv.org/abs/2111.06464): noise alone induces compositionality. |
| **H1** — dynamic reliability favours redundant coordination | As stated, close to the published result above. Survives only if restated against *state-dependent* transmission from measured profiles. |
| **H6** — calibration burden rather than offline accuracy | **Substantially claimed.** The [FALCON benchmark](https://openreview.net/forum?id=FN02v4nD8y) (NeurIPS 2024) already standardises few-shot cross-session intracortical decoding with held-out sessions carrying deliberately insufficient data. An [MS-ITR metric](https://pmc.ncbi.nlm.nih.gov/articles/PMC9954620/) already scores performance against calibration cost on the same argument the README makes. FALCON was not cited in this repository until now. |
| **H4** — competence retained while developmental lineage is recoverable from an external trace but not from current state | **Appears open** (`MODELLED`). Adjacent work asks whether training history can be recovered *from weights* — [Approximating LM Training Data from Weights](https://arxiv.org/html/2506.15553), [Model Tree Heritage Recovery](https://arxiv.org/pdf/2405.18432), [developmental interpretability](https://devinterp.com/). All are capability questions. H4 asks about a *dissociation*, which did not surface. |
| **Interface between representation-rich systems** | **Active field.** Nearest: [Latent Communication Between Language Model Agents](https://arxiv.org/html/2607.14103) — dense residual-stream vs SAE-sparse vs text channels between Llama and Mistral. Read directly, it models **no** channel noise, **no** biological constraint, and studies **only final trained states**. |

---

## 4. The interface objection, stated precisely

The author's objection — that the model treats the dendrite as isolated from the
system of intelligence preceding it — is correct and is the most consequential of
the three.

With a representationally rich backend, several things change character rather
than degree:

- Similar meanings have similar representations, so a code can **exploit**
  structure rather than inventing arbitrary labels.
- Errors become **semantically graded**: substituting a nearby symbol costs less
  than a distant one, which is what happens biologically and nothing like the
  uniform-cost substitution implemented.
- Topographic similarity becomes measurable, because a geometry finally exists.
- "Unknown common ground" stops being a dial and becomes an empirical property of
  two systems with genuinely non-identical representations.

The question shifts from *can two blank agents invent a code under noise*
(answered, repeatedly) to *what survives a constrained interface between systems
that already know things*.

---

## 5. The parallelism objection

Also correct, and it is the same error in different form. The relevant redesign
is **N parallel unreliable channels with population integration** rather than a
serial token stream. Consequences that then follow structurally rather than by
engineering:

- Redundancy under unreliability becomes emergent, not a budget parameter.
- Bounded signalling becomes an actual bandwidth constraint in bits.
- Channel dropout is literally electrode/channel loss, unifying the abstract and
  applied ends of the fidelity ladder.
- Sparsity and graceful degradation — the properties §7 cares about — become
  available at all.

---

## 6. The Allen Institute model, and the goal mismatch

`MEASURED` — full preprint read.

[Ito, Haufler, Galván Fraile, Dai, Aman, Chen, Mirasso, Maass & Arkhipov (2026)](https://www.biorxiv.org/content/10.64898/2026.03.13.711751v1),
*Deep-learning-assisted simulation of a cortical circuit*: a differentiable
~67,000-neuron mouse V1 model, 19 cell types, constrained by EM connectomics,
multipatch synaptic physiology, cell-type electrophysiology and Neuropixels
recordings. Trains end-to-end in ~10 hours on one mainstream GPU. Code and trained
parameters at `AllenInstitute/biorealistic-v1-model`. It uses
[Campagnola et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9970277/) —
this project's own citation — as its synaptic constraint.

**This occupies fidelity level 3.** Building a competing mouse V1 circuit model
would be wasted effort.

### What it does not model

| Mechanism | Status in that model |
|---|---|
| Short-term plasticity | Absent; the phrase does not occur in the paper |
| Stochastic / quantal release | Absent. Weights are log-normal fits to PSP amplitudes at the 90th-percentile pulse response "under elevated release probability" — release probability collapsed to a static point estimate in the *high-release* regime |
| Dendritic computation | Absent. 201 GLIF Type-3 point models. Dendritic extent enters only as a statistical correction to weight assignment |
| Human | Absent as a modelled arm; appears only in reference titles |
| Synaptic state | Further compressed, 44 → 8 postsynaptic-current states per neuron, for BPTT memory |

### Their framing, which is worth adopting

Their central methodological result:

> "Removing biological priors on synaptic weight distributions does not prevent
> the network from matching aggregate firing-rate and selectivity targets, yet it
> alters the emergent synaptic rules and collapses cell-type-specific
> differences… constraints from synaptic physiology act not merely as
> regularizers but as **selectors among functionally equivalent solutions**."

Biological constraints are about **identifiability**, not fit. Many
parameterizations satisfy the same activity targets; the constraint decides which
one you land in.

Their other headline: inhibitory cohorts *"emerge through training rather than
from initialization."* A developmental claim, established by comparing endpoint
against initialization — the thinnest possible trace. They never ask whether the
route is recoverable from the final weights. **That is H4, made concrete, on a
real circuit, with open code.**

### The goal mismatch

Arkhipov's group appears aimed at mechanistic understanding of cortical function,
with ablation as a lesion analogue — plausibly toward neurological conditions.
The author's aim is architectural transfer for efficiency. Same substrate,
different destination. The overlap is real but partial, and the divergence
matters: a model can be biologically excellent and say nothing about efficiency.

---

## 7. Prior art on the actual goal

`MEASURED`. This is where the author's intuitions must be tested, and both core
ones are already established.

**Stochastic release as an efficiency mechanism** is a developed line:
[Neftci et al. (2016)](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2016.00241/full)
(Synaptic Sampling Machines — stochasticity as both Monte Carlo sampling and
DropConnect-style regularization);
[presynaptic stochasticity work (2021)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8716105/)
(release probabilities encode synaptic importance; energy allocated sparsely to
synapses that matter);
[Signatures of Bayesian inference from energy-efficient synapses](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11302983/)
(trainable stochastic synapses with explicit energetic cost; explicit
performance/reliability tradeoff). The observation that synaptic failure lowers
energy without lowering transmitted information is theirs.

**Human dendritic compartmentalization as computational density** is also live.
Human L2/3 pyramidal cells sustain ~25 independent simultaneous NMDA spikes
against ~14 in rat; mouse spine density is ~2.6× human. A paper already implements
human-versus-mouse neuronal structural differences in generative models
([arXiv 2410.20735](https://arxiv.org/pdf/2410.20735)).

**Consequence.** "Add synaptic stochasticity for efficiency" is not a novel
proposal. Any claim of novelty must be narrower than that.

---

## 8. What appears to remain open

`HYPOTHESIS` — these are the load-bearing claims and the ones most needing a
second opinion.

**8.1 Measured parameterization versus hand-tuned abstraction.** Every efficiency
result in §7 uses a designed abstraction: a tunable scalar release probability, a
generic two-compartment dendrite. No work found asks whether the **measured,
cell-type-resolved, species-specific** parameterization behaves differently.

That question is newly askable because three things now coexist: Campagnola-grade
measured synaptic dynamics per connection type in mouse *and* human; a
differentiable data-constrained circuit that can be trained; and Arkhipov's
finding that biological constraints select among functionally equivalent
solutions.

> **Does biology's measured parameterization select a more energy-efficient
> solution than hand-tuned abstractions do?**

If yes, the transferable result is not "add noise" — it is "adopt the specific
*structure* of biological unreliability."

**8.2 Multi-modality.** The efficiency literature is single-modality — MNIST,
CIFAR, one input statistic. Contemporary AI spends most of its energy on
*generality*: retraining, fine-tuning, per-task specialization. If a biological
parameterization is efficient across input statistics where hand-tuned ones need
per-task retuning, that is a materially stronger claim, and it connects to
cortical uniformity. The author's insistence on varied signal structures is
therefore load-bearing, not decorative.

**8.3 Human as donor rather than comparator.** The field defaults to mouse for
tractability. For architectural transfer the relevant donor is the one achieving
more with less — fewer spines, greater dendritic compartmentalization, more local
computation. That inverts the default and is correct for this goal.

---

## 9. What must change in the project

1. **Restate the goal.** The README describes neuroscience understanding. It
   should describe efficiency-principle extraction validated for transfer.
2. **Add efficiency to the validation contract.** `docs/validation.md` currently
   contains **no** efficiency metric — it measures fidelity only. Energy per unit
   task performance, operations per inference, activation sparsity, and bits per
   joule are primary for this goal, and absent.
3. **Add an efficiency axis orthogonal to the fidelity ladder.** A level-3 model
   can be biologically faithful and silent on efficiency. Conflating the two
   produces a simulator rather than an architecture.
4. **Promote the human profile from comparative constraint to primary target**;
   mouse becomes the tractability fallback.
5. **Make multi-modal input a first-class experimental requirement**, not a later
   generalization test.
6. **Do not rebuild level 3.** Adopt the Allen model.
7. **Move the centre of gravity** from `experiments/synaptic_emergence` to the
   dynamic-synapse work, built against a real circuit rather than a toy channel.

---

## 10. Technical notes bearing on feasibility

- **Short-term plasticity (Tsodyks–Markram) is differentiable** — a deterministic
  dynamical system on synaptic state. It should attach to a differentiable
  simulator without a rewrite. This is the cheap first experiment.
- **Stochastic release breaks differentiability.** Training through it needs a
  relaxation — reparameterization, straight-through, or surrogate gradients. This
  is genuinely hard, and *is itself plausibly a contribution*: a differentiable
  stochastic synapse for large-scale circuit training was not found in the scan.
- **Energy accounting is treacherous.** Brain-versus-GPU comparisons routinely
  compare incommensurable quantities across different substrates and tasks, and
  the brain is not running backpropagation. Any efficiency number needs a
  declared accounting *before* it is reported. The project's existing evidence
  discipline is well suited to this and most neuromorphic work lacks it.

---

## 11. Weaknesses of this critique

Stated plainly so a reviewer can calibrate.

- **The prior-art scan was targeted, not systematic.** Findings of "not found" are
  weaker than "does not exist."
- **It already failed once in exactly this way.** The first pass searched the ML
  and emergent-communication literature and never asked who had already built
  level 3; it missed the Allen preprint entirely, which the author supplied. A
  systematic review by someone fluent in *all* of computational neuroscience,
  neuromorphic engineering, and emergent communication is still required.
- **Neuromorphic hardware was not surveyed.** Loihi, TrueNorth, SpiNNaker,
  BrainScaleS and the SNN training literature were not examined, and §7–8 could
  be substantially undermined by work there. This is the largest known gap.
- **Wolfgang Maass is a co-author on the Allen paper** and is foundational in
  spiking networks and stochastic computation in the brain. His prior work was not
  reviewed and is likely to bear directly on §8.1.
- **The Allen preprint's results section was skimmed**, not read line by line;
  methods, abstract and discussion were read closely.
- **§8 rests on absence of evidence** and is the part most likely to be wrong.
- **No claim here has been tested by running anything.** Every efficiency
  statement is from literature, not measurement.

---

## 12. Questions for the reviewer

1. Is §8.1 — measured parameterization versus hand-tuned abstraction — a real
   distinction, or a distinction without a difference? This is the central claim.
2. What does the neuromorphic and SNN literature already say about §8.1 and §8.2?
   This is the acknowledged blind spot.
3. Is the identifiability framing borrowed from Arkhipov (§6) the right frame for
   an efficiency goal, or does it smuggle in a fidelity objective that quietly
   competes with efficiency?
4. Is human-as-donor (§8.3) defensible given how much less human data exists, or
   does data scarcity make it impractical regardless of being conceptually right?
5. Is the efficiency question separable from the coordination question at all? The
   original intent concerned *signalling between systems*; §8 concerns *efficient
   computation within one*. These may be different projects wearing one name — and
   failing to separate them is how this drifted the first time.
6. **Is the intended output an architectural principle that could be handed to
   someone building models, or a working efficient system?** These diverge almost
   immediately: the first is a study with a falsifiable claim, the second an
   engineering programme in which the biology is scaffolding to be discarded.
   The project cannot be scoped until this is settled.
