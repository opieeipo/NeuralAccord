# Biological constraints

The initial biological target is **cortical microcircuit dynamics**, not a
generic model of "the brain."

## Profiles

| Profile | Role | Rationale |
|---|---|---|
| Mouse cortex | Initial mechanistic baseline | Strongest experimentally tractable mammalian foundation linking cell type, connectivity, synaptic physiology, plasticity, behavior, and perturbation |
| Human cortex | Comparative constraint | Tests transfer rather than assuming mouse is an interchangeable human proxy |
| Comparative profile | Uncertainty and transfer experiments | Holds task and analysis constant while changing documented species constraints |

Mouse and human evidence stay in separate files. They are never averaged into
an undocumented mammalian default.

## Fidelity ladder

The ladder governs what a run is *allowed to conclude*, independently of how
good its numbers look.

| Level | Implementation | Permitted conclusion |
|---|---|---|
| 0 — Functional | Discrete events; bounded signaling; erasure and interference; reward-driven adaptation | Computational effects of constrained stochastic communication |
| 1 — Dynamic synapse | State-dependent release; facilitation; depression; delay; parameter distributions | Consequences of modeled synaptic dynamics for Level 0 phenomena |
| 2 — Population code | Spiking/rate populations; probabilistic synapses; inhibition; temporal decoding | Whether phenomena survive without designer-defined symbols |
| 3 — Circuit-specific | Named region, layer, cell types, connectivity, plasticity, validation targets | A declared circuit model under specified conditions — not a whole-brain model |
| 4 — BCI co-adaptation | Historical recordings, limited current-session labels, closed-loop simulation, task-specific baselines | Whether an approach lowers calibration burden under declared data and evaluation conditions |

A configuration declares its `fidelity_level`. A report that draws a Level 2
conclusion from a Level 0 run is a defect, not a stretch.

## Validation targets

A profile at Level 3 declares what it is checked against — firing rates,
connection probabilities, short-term plasticity — and biological validation
error is reported per target rather than aggregated into one score.

## Declared omissions

Each profile lists what it does not model. Current standing omissions across
the skeleton profiles: neuromodulation, glial contributions, dendritic
nonlinearity, and developmental time course. Omissions are published, not
discovered by a reader.
