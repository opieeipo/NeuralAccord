"""The ``neural-accord`` command line entry point.

Two verbs are declared in the README and wired here:

    neural-accord run configs/mouse/v1_l23_dynamic_synapse.yaml --seed 1042
    neural-accord bci-evaluate configs/bci/cursor_cross_session.yaml --seed 1042

Both currently load and validate the experiment declaration, resolve it, and
stop. Executing an experiment is deliberately not implemented: the first
deliverable is a tested Level 0 baseline, and a command that silently produces
numbers before that exists would be worse than one that refuses.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from core import __version__
from core.config import ConfigError, load_experiment
from core.i18n import _, activate
from core.reproducibility.seeds import seed_manifest


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for the ``neural-accord`` command."""
    parser = argparse.ArgumentParser(
        prog="neural-accord",
        description=_("Run reproducible experiments under declared biological constraints."),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"neural-accord {__version__}",
    )
    parser.add_argument(
        "--lang",
        metavar=_("LOCALE"),
        help=_("Language for messages, e.g. 'de' or 'zh-Hans'. Defaults to your environment."),
    )

    subcommands = parser.add_subparsers(dest="command", required=True)

    run = subcommands.add_parser(
        "run",
        help=_("Run a biological experiment from a versioned YAML declaration."),
    )
    run.add_argument("config", type=Path, metavar=_("CONFIG"))
    run.add_argument(
        "--seed",
        type=int,
        action="append",
        metavar=_("N"),
        help=_("Seed to run. Repeat the option to run a seed list."),
    )

    bci = subcommands.add_parser(
        "bci-evaluate",
        help=_("Evaluate calibration burden on a chronological cross-session split."),
    )
    bci.add_argument("config", type=Path, metavar=_("CONFIG"))
    bci.add_argument(
        "--seed",
        type=int,
        action="append",
        metavar=_("N"),
        help=_("Seed to run. Repeat the option to run a seed list."),
    )

    return parser


def _describe(config_path: Path, seeds: Sequence[int]) -> str:
    """Summarize what an invocation would run, for the operator's benefit."""
    lines = [_("Experiment declaration: {path}").format(path=config_path)]
    manifest = seed_manifest(seeds)
    lines.append(
        _("Seeds requested: {count}").format(count=len(manifest))
        if manifest
        else _("No seed given; a reported result requires a seed list, not one best run.")
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point. Returns a process exit status."""
    args = build_parser().parse_args(argv)
    activate(args.lang)

    seeds: list[int] = args.seed or []

    try:
        experiment = load_experiment(args.config)
    except ConfigError as error:
        print(_("Configuration error: {reason}").format(reason=error), file=sys.stderr)
        return 2

    print(_describe(args.config, seeds))
    print(_("Declared fidelity level: {level}").format(level=experiment.get("fidelity_level", "?")))
    print(
        _(
            "Execution is not implemented yet. This release scaffolds the "
            "reproducibility contract only; see docs/validation.md for what a "
            "result must carry before it can be reported."
        ),
        file=sys.stderr,
    )
    return 3


if __name__ == "__main__":  # pragma: no cover - exercised via the console script
    raise SystemExit(main())
