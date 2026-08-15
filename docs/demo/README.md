# Interactive pages

Three self-contained pages that accompany the platform. They share one token
system — palette, type scale, and panel structure — so they read as one family.

| Page | What it is |
|---|---|
| `synaptic-emergence.html` | The project's **blank-slate control condition**, run live. Two systems with no prior representation of the world form a convention through a channel that erases and corrupts, with the no-communication and randomized-communication controls alongside. Reproduces a known result deliberately — see [`../related-work.md`](../related-work.md). |
| `fidelity-ladder.html` | An explainer: what each fidelity level permits you to conclude, the four evidence labels, and the constraint map. |
| `calibration-burden.html` | An explainer: why B<sub>τ</sub> rather than offline accuracy is the unit of claim in the BCI track. |

## What these pages are not

The Level 0 page runs a real simulation, but it is a **browser reimplementation
for illustration** and carries no evidentiary weight. It has one seed, no
variance across seeds, and no resolved configuration. The authoritative
implementation is the Python package; anything reportable comes from
`neural-accord run` under the contract in [`../validation.md`](../validation.md).

The calibration-burden curves are **synthetic** — closed-form functions chosen
to make the argument legible. No recording is involved, and no real dataset is
referenced or redistributed.

## Source format

Each file is a page **fragment**: a `<title>`, a `<style>` block, markup, and a
`<script>`. There is deliberately no `<!doctype>`, `<html>`, `<head>`, or
`<body>` — that skeleton is added at build time, which keeps one source per page
rather than two copies that drift apart.

To produce standalone documents for static hosting:

```bash
python3 docs/demo/build.py            # writes docs/demo/_site/ (gitignored)
python3 -m http.server -d docs/demo/_site 8000
```

## Conventions worth keeping

- **Canvases carry `data-h`, never a `height` attribute.** Assigning
  `canvas.height` writes back to the attribute, so a sizing routine that reads
  the attribute sees the device-pixel-scaled value and doubles the element on
  every redraw.
- **Every colour token is defined on bare `:root`.** A token defined only inside
  `@media (prefers-color-scheme: dark)` is undefined for viewers on the default
  "system" setting, which renders one theme's text on the other theme's ground.
- **Categorical colours are validated, not eyeballed** — for lightness band,
  chroma floor, colour-vision-deficiency separation, and surface contrast.
- **Evidence labels are ordinal**, and encoded by fill weight and border style
  as well as hue, so the ranking survives without colour.

`tests/test_demo_pages.py` enforces the first three, plus that every inline
script actually parses. That last check exists because a quoting error once
shipped a page whose script never ran: every control dead, every canvas blank,
and the surrounding HTML looking entirely fine.
