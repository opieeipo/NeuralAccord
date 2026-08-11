# Provenance

How a value gets into Neural Accord, and what has to travel with it.

## The rule

No biological parameter enters a profile without all of:

| Field | Meaning |
|---|---|
| `species` | Named species. Not "mammal". |
| `region` | Named region. Not "cortex" alone where a region is known. |
| `cortical_layer` | Layer, where the source specifies one. |
| `cell_class` / `connection_class` | Pre- and postsynaptic identity. |
| `conditions` | Temperature, age, preparation, recording method, stimulus protocol. |
| `source` | Citation resolvable in `references.bib`. |
| `uncertainty` | Spread as reported, not a point estimate stripped of its error. |
| `evidence` | One of `MEASURED`, `MODELLED`, `ABSTRACTED`, `HYPOTHESIS`. |

A value missing any of these is recorded as `unknown`. An `unknown` is a
result, not a failure — it bounds what the model may conclude.

## No mammalian default

Where a human parameter is unavailable, it is recorded as one of:

- `unknown` — no usable source.
- `inferred` — derived from other measured values, with the derivation written
  down.
- `mouse_prior_for_sensitivity_only` — borrowed solely to bound a sensitivity
  analysis. Any result from such a sweep is reported as a sensitivity bound and
  never as a human measurement.

Silently copying a mouse value into a human profile is the specific failure
this document exists to prevent.

## Datasets

Large raw data never enter Git. The repository holds:

- a manifest naming the dataset, version, and access terms;
- checksums for every file the analysis reads;
- the transformations applied, in order;
- the citation.

Controlled human BCI data are not redistributed outside their governing
data-use agreement, in any form, including derived features that would permit
reconstruction.

## Recording a source

Sources live in `docs/references.bib`, managed through Zotero. A profile entry
references the BibTeX key; it does not restate the citation inline.

## Status

Skeleton. The first profiles to populate are `profiles/mouse/v1_l23.yaml` and
then `profiles/human/v1_l23.yaml`.
