"""Guards for the interactive pages under ``docs/demo/``.

These exist because a quoting error in an inline script once shipped a page
whose JavaScript never parsed: every control was dead and every canvas blank,
while the HTML around it looked perfectly fine. Nothing in the Python suite
could have caught it, so these tests do.
"""

from __future__ import annotations

import itertools
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


# --------------------------------------------------------------------------
# Behavioural checks on the Level 0 simulation itself.
#
# The page makes claims in prose — that the controls sit at chance, that
# redundancy helps under heavy erasure, that private episodes are withheld from
# learning. These run the shipped simulation and check the claims hold, so the
# page cannot quietly start saying something the code no longer does.
# --------------------------------------------------------------------------

LEVEL0 = DEMO_DIR / "synaptic-emergence.html"

HARNESS = """
const fs = require("node:fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const core = html.slice(
  html.indexOf("function mulberry32"),
  html.indexOf("/* ---------------- state ----------------")
);
const makeSystem = new Function(core + "\\nreturn makeSystem;")();

function run(overrides, episodes) {
  const cfg = { K: 8, V: 8, B: 1, pE: 0, pS: 0, pPriv: 0, lr: 0.08, ...overrides };
  const sys = makeSystem(cfg, overrides.mode || "pair", overrides.seed ?? 1042);
  sys.run(episodes, false);
  return { acc: sys.accuracy, comm: sys.commAccuracy, chance: 1 / cfg.K };
}

// the ceiling and regime functions exactly as the page defines them
const fnStart = html.indexOf("  // The best accuracy any strategy could reach");
const fnEnd = html.indexOf("  function paint()");
const { channelCeiling, regime } = new Function(
  html.slice(fnStart, fnEnd) + "\\nreturn { channelCeiling, regime };"
)();

function bound(overrides, episodes, seeds) {
  const cfg = { K: 8, V: 8, B: 1, pE: 0, pS: 0, pPriv: 0, lr: 0.08, ...overrides };
  let acc = 0;
  for (let i = 0; i < seeds; i++) {
    const sys = makeSystem(cfg, "pair", 1042 + i * 7919);
    sys.run(episodes, false);
    acc += sys.accuracy;
  }
  return { acc: acc / seeds, ceiling: channelCeiling(cfg), chance: 1 / cfg.K };
}

const SWEEP = [
  {}, { pE: 0.15 }, { pE: 0.3, pS: 0.15 }, { pE: 0.5, pS: 0.2 },
  { pS: 0.5 }, { V: 2 }, { V: 4 }, { K: 2 }, { V: 12, K: 4 },
  { B: 2 }, { B: 2, pE: 0.65 }, { B: 2, pE: 0.3, pS: 0.15 }, { B: 2, V: 2 },
];

const out = {
  clean: run({}, 60000),
  noComms: run({ mode: "none" }, 60000),
  randomComms: run({ mode: "rand" }, 60000),
  budget1: run({ pE: 0.65, B: 1 }, 60000),
  budget2: run({ pE: 0.65, B: 2 }, 60000),
  deadChannelPrivate: run({ pE: 0.9, pPriv: 0.9 }, 60000),
  sweep: SWEEP.map((o) => ({ cfg: o, ...bound(o, o.B === 2 ? 120000 : 90000, 3) })),
  labels: {
    converged: regime(0.632, 0.125, channelCeiling({ K: 8, V: 8, B: 1, pE: 0.3, pS: 0.15 }))[0],
    early: regime(0.20, 0.125, channelCeiling({ K: 8, V: 8, B: 1, pE: 0.3, pS: 0.15 }))[0],
    atChance: regime(0.125, 0.125, channelCeiling({ K: 8, V: 8, B: 1, pE: 0.3, pS: 0.15 }))[0],
    noCapacity: regime(0.147, 0.125, channelCeiling({ K: 8, V: 8, B: 1, pE: 0.9, pS: 0.6 }))[0],
  },
  hysteresis: (() => {
    const cfg = { K: 8, V: 8, B: 1, pE: 0.3, pS: 0.15 };
    const chance = 1 / cfg.K;
    const ceiling = channelCeiling(cfg);
    const at = (lift) => chance + lift * (ceiling - chance);
    const label = (lift, band) => regime(at(lift), chance, ceiling, band);

    // walk a noisy climb through the Forming/Coordinated boundary
    let band = null;
    const climb = [];
    for (const lift of [0.5, 0.78, 0.82, 0.79, 0.83, 0.86, 0.9, 0.84, 0.78, 0.74, 0.6]) {
      const r = label(lift, band);
      band = r[2];
      climb.push(r[0]);
    }

    // a run that never left the bottom must still read as collapsed
    let low = null;
    const floor = [];
    for (const lift of [0.02, 0.09, 0.05, 0.11, 0.03]) {
      const r = label(lift, low);
      low = r[2];
      floor.push(r[0]);
    }

    return {
      climb,
      floor,
      freshAt082: label(0.82, null)[0],
      stickyAt082: label(0.82, 2)[0],
      promotedAt086: label(0.86, 2)[0],
      stickyAt078: label(0.78, 3)[0],
      demotedAt072: label(0.72, 3)[0],
    };
  })(),
};
console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def sim(node: str, tmp_path_factory: pytest.TempPathFactory) -> dict:
    if not LEVEL0.is_file():
        pytest.skip("Level 0 page not present")
    harness = tmp_path_factory.mktemp("sim") / "harness.cjs"
    harness.write_text(HARNESS, encoding="utf-8")
    result = subprocess.run(
        [node, str(harness), str(LEVEL0)],
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert result.returncode == 0, result.stderr
    import json

    return json.loads(result.stdout)


def test_a_convention_forms_on_a_clean_channel(sim: dict) -> None:
    assert sim["clean"]["acc"] > 0.9


def test_both_controls_sit_at_chance(sim: dict) -> None:
    """A control above chance would mean information is leaking around the channel."""
    chance = sim["noComms"]["chance"]
    for key in ("noComms", "randomComms"):
        assert abs(sim[key]["acc"] - chance) < 0.05, f"{key} is not at chance"


def test_redundancy_helps_under_heavy_erasure(sim: dict) -> None:
    """H1, as the page states it: a second symbol buys robustness when the
    channel is unreliable."""
    assert sim["budget2"]["acc"] > sim["budget1"]["acc"] + 0.02


def test_private_episodes_are_withheld_from_learning(sim: dict) -> None:
    """The reward-leakage control: with a dead channel and mostly private
    observation, overall accuracy is high while nothing was learned through the
    channel. The regime tile must classify on the comms-only figure, or it
    reports a stable convention where there is none."""
    case = sim["deadChannelPrivate"]
    assert case["acc"] > 0.7, "expected private observation to inflate overall accuracy"
    assert case["comm"] < case["chance"] + 0.08, "channel should have taught nothing"
    assert case["acc"] - case["comm"] > 0.4, "the two figures should diverge sharply"


def test_regime_is_classified_on_comms_only(sim: dict) -> None:
    """Guards the specific defect: classifying on overall accuracy made the
    dead-channel case read 'Coordinated' instead of 'Collapse'."""
    source = LEVEL0.read_text(encoding="utf-8")
    assert "const basis = accC == null ? acc : accC;" in source, (
        "the regime basis must be the comms-only figure"
    )
    assert "regime(basis, chance, ceiling, regimeBand)" in source, (
        "regime must be called with that basis, not overall accuracy"
    )

    case = sim["deadChannelPrivate"]
    chance = case["chance"]
    lift_overall = (case["acc"] - chance) / (1 - chance)
    lift_comms = (case["comm"] - chance) / (1 - chance)
    assert lift_overall >= 0.8, "this case should look 'Coordinated' on overall accuracy"
    assert lift_comms < 0.08, "and 'Collapse' on comms-only, which is what must be shown"


def test_ceiling_bounds_the_simulation(sim: dict) -> None:
    """The analytic ceiling must be an upper bound the learner approaches but
    never passes. A ceiling that a run can exceed would make the regime
    meaningless; one far above the run would make it unreachable."""
    over: list[str] = []
    slack: list[str] = []
    for case in sim["sweep"]:
        # 1 SE of the page's 400-episode rolling mean is about 0.025.
        if case["acc"] > case["ceiling"] + 0.03:
            over.append(f"{case['cfg']}: {case['acc']:.3f} > ceiling {case['ceiling']:.3f}")
        room = case["ceiling"] - case["chance"]
        if room > 0.05:
            reached = (case["acc"] - case["chance"]) / room
            if reached < 0.7:
                slack.append(f"{case['cfg']}: reached only {reached:.0%} of ceiling")
    assert not over, "ceiling is not an upper bound: " + "; ".join(over)
    assert not slack, "ceiling is unreachably loose: " + "; ".join(slack)


def test_converged_run_at_defaults_reads_as_coordinated(sim: dict) -> None:
    """The defect this replaced: measuring against 1.0 meant a run sitting at
    the channel's ceiling was labelled 'convention consolidating' forever."""
    assert sim["labels"]["converged"] == "Coordinated"


def test_regime_still_distinguishes_early_and_chance_runs(sim: dict) -> None:
    assert sim["labels"]["early"] == "Partial"
    assert sim["labels"]["atChance"] == "Collapse"


def test_negligible_capacity_is_not_graded(sim: dict) -> None:
    """When the ceiling sits within noise of chance the ratio is meaningless,
    so the regime reports the channel rather than grading the pair."""
    assert sim["labels"]["noCapacity"] == "No capacity"


def test_regime_does_not_chatter_across_a_boundary(sim: dict) -> None:
    """A noisy climb through the Forming/Coordinated boundary must produce one
    transition, not a run of flips. The lift estimate carries about +/-0.05 of
    sampling noise, so a bare threshold flickers whenever a run is passing one --
    most visibly at high meaning counts, where learning lingers near a boundary.
    """
    climb = sim["hysteresis"]["climb"]
    changes = sum(1 for a, b in itertools.pairwise(climb) if a != b)
    assert changes <= 2, f"label changed {changes} times over one climb: {climb}"


def test_hysteresis_needs_an_overshoot_to_promote(sim: dict) -> None:
    h = sim["hysteresis"]
    assert h["stickyAt082"] == "Forming", "0.82 should not yet promote from Forming"
    assert h["promotedAt086"] == "Coordinated", "0.86 should promote"
    assert h["freshAt082"] == "Coordinated", "with no prior band, 0.82 classifies plainly"


def test_hysteresis_needs_an_undershoot_to_demote(sim: dict) -> None:
    h = sim["hysteresis"]
    assert h["stickyAt078"] == "Coordinated", "0.78 should not yet demote"
    assert h["demotedAt072"] == "Forming", "0.72 should demote"


def test_a_run_at_the_floor_still_reads_as_collapse(sim: dict) -> None:
    """Stickiness must not suppress the collapse label -- the project reports
    collapse regimes as results, so they cannot be smoothed away."""
    assert set(sim["hysteresis"]["floor"]) == {"Collapse"}, sim["hysteresis"]["floor"]
