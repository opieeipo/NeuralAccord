"""Guards for the interactive pages under ``docs/demo/``.

These exist because a quoting error in an inline script once shipped a page
whose JavaScript never parsed: every control was dead and every canvas blank,
while the HTML around it looked perfectly fine. Nothing in the Python suite
could have caught it, so these tests do.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "docs" / "demo"
PAGES = sorted(DEMO_DIR.glob("*.html"))

SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)
STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)

pytestmark = pytest.mark.skipif(not PAGES, reason="no demo pages present")


def page_ids(path: Path) -> str:
    return path.stem


@pytest.fixture(scope="module")
def node() -> str:
    exe = shutil.which("node")
    if not exe:
        pytest.skip("node is not installed; cannot syntax-check inline scripts")
    return exe


@pytest.mark.parametrize("page", PAGES, ids=page_ids)
def test_inline_script_parses(page: Path, node: str, tmp_path: Path) -> None:
    """The inline script must be syntactically valid JavaScript."""
    scripts = SCRIPT_RE.findall(page.read_text(encoding="utf-8"))
    assert scripts, f"{page.name} has no inline script"

    for index, source in enumerate(scripts):
        target = tmp_path / f"{page.stem}-{index}.js"
        target.write_text(source, encoding="utf-8")
        result = subprocess.run(
            [node, "--check", str(target)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"{page.name} script {index}:\n{result.stderr}"


@pytest.mark.parametrize("page", PAGES, ids=page_ids)
def test_page_is_a_fragment(page: Path) -> None:
    """Sources are fragments; the document skeleton is added by build.py."""
    head = page.read_text(encoding="utf-8")[:4096].lower()
    for tag in ("<!doctype", "<html", "<head>", "<body>"):
        assert tag not in head, f"{page.name} should not declare {tag}"


@pytest.mark.parametrize("page", PAGES, ids=page_ids)
def test_page_has_a_title(page: Path) -> None:
    assert re.search(r"<title>.+</title>", page.read_text(encoding="utf-8"))


@pytest.mark.parametrize("page", PAGES, ids=page_ids)
def test_theme_tokens_are_defined_outside_media_queries(page: Path) -> None:
    """Every colour token needs a definition on bare ``:root``.

    A token defined only inside ``@media (prefers-color-scheme: dark)`` or a
    ``[data-theme]`` block is undefined for viewers on the default "system"
    setting, which renders one theme's text on the other theme's background.
    """
    styles = "\n".join(STYLE_RE.findall(page.read_text(encoding="utf-8")))
    assert styles, f"{page.name} has no inline styles"

    bare = re.search(r":root\s*\{(.*?)\}", styles, re.S)
    assert bare, f"{page.name} has no bare :root block"
    defined = set(re.findall(r"(--[\w-]+)\s*:", bare.group(1)))

    used = set(re.findall(r"var\((--[\w-]+)", styles))
    missing = sorted(used - defined)
    assert not missing, f"{page.name}: tokens used but never defined on bare :root: {missing}"


@pytest.mark.parametrize("page", PAGES, ids=page_ids)
def test_canvases_declare_a_logical_height(page: Path) -> None:
    """Canvases must carry ``data-h`` rather than a ``height`` attribute.

    Assigning ``canvas.height`` writes back to the ``height`` attribute, so a
    sizing routine that reads the attribute would see the device-pixel-scaled
    value and double the element on every redraw.
    """
    text = page.read_text(encoding="utf-8")
    for tag in re.findall(r"<canvas\b[^>]*>", text):
        assert "height=" not in tag, f"{page.name}: canvas uses height attribute: {tag}"
        assert "data-h=" in tag, f"{page.name}: canvas missing data-h: {tag}"


def test_build_script_produces_standalone_pages(tmp_path: Path) -> None:
    """build.py must wrap every fragment into a servable document."""
    result = subprocess.run(
        ["python3", str(DEMO_DIR / "build.py"), "--out", str(tmp_path / "site")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    out = tmp_path / "site"
    assert (out / "index.html").is_file()
    for page in PAGES:
        built = out / page.name
        assert built.is_file(), f"{page.name} was not built"
        text = built.read_text(encoding="utf-8")
        assert text.startswith("<!doctype html>")
        assert "<title>" in text
        assert text.count("<title>") == 1, f"{page.name} built with a duplicate title"
