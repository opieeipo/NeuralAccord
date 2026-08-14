#!/usr/bin/env python3
"""Wrap the demo page fragments into standalone HTML for static hosting.

The sources in this directory are page *fragments*: a ``<title>``, a ``<style>``
block, markup, and a ``<script>``, with no ``<!doctype>``/``<html>``/``<head>``/
``<body>`` of their own. That is the form the artifact publisher expects, and
keeping one source per page avoids two copies drifting apart.

This script adds the document skeleton so the same files can be served from
GitHub Pages or opened locally:

    python3 docs/demo/build.py            # writes docs/demo/_site/
    python3 docs/demo/build.py --out DIR  # writes elsewhere

Nothing here is required to publish an artifact; it exists so the repository can
host the pages itself.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<style>
  /* Minimal reset, matching what the artifact host supplies. */
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ -webkit-text-size-adjust: 100%; }}
  body {{ margin: 0; }}
  img, svg, canvas {{ max-width: 100%; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""

DESCRIPTIONS = {
    "synaptic-emergence": (
        "A live Level 0 signalling experiment: convention formation through a channel "
        "that erases and corrupts, with controls."
    ),
    "fidelity-ladder": (
        "What each level of the Neural Accord fidelity ladder lets you conclude, and "
        "where each mechanism stops being a biological claim."
    ),
    "calibration-burden": (
        "Why calibration burden, not offline accuracy, is the unit of claim for a "
        "brain-computer interface decoder."
    ),
}


def title_of(text: str, fallback: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, re.S)
    return match.group(1).strip() if match else fallback


def build(out: Path) -> int:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    pages = sorted(p for p in HERE.glob("*.html"))
    if not pages:
        print("no page fragments found")
        return 1

    for page in pages:
        text = page.read_text(encoding="utf-8")
        stem = page.stem
        title = title_of(text, stem)
        body = re.sub(r"<title>.*?</title>\s*", "", text, count=1, flags=re.S)
        (out / page.name).write_text(
            SKELETON.format(
                title=title,
                description=DESCRIPTIONS.get(stem, title),
                content=body.strip(),
            ),
            encoding="utf-8",
        )
        print(f"wrote {out / page.name}  ({title})")

    index = "\n".join(
        f'    <li><a href="{p.name}">{title_of(p.read_text(encoding="utf-8"), p.stem)}</a></li>'
        for p in pages
    )
    (out / "index.html").write_text(
        SKELETON.format(
            title="Neural Accord — demo and explainers",
            description="Interactive pages accompanying the Neural Accord research platform.",
            content=(
                '  <main style="font-family: system-ui, sans-serif; max-width: 40rem; '
                'margin: 4rem auto; padding: 0 1.5rem; line-height: 1.6;">\n'
                "    <h1>Neural Accord</h1>\n"
                "    <p>Interactive pages accompanying the research platform.</p>\n"
                f"    <ul>\n{index}\n    </ul>\n"
                "  </main>"
            ),
        ),
        encoding="utf-8",
    )
    print(f"wrote {out / 'index.html'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "_site")
    return build(parser.parse_args().out)


if __name__ == "__main__":
    raise SystemExit(main())
