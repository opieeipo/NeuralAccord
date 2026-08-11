"""Loading and validating experiment declarations.

Every experiment is declared in YAML and must resolve to a fully specified
configuration before anything runs. This module holds the minimum contract:
the file parses, it carries an ``experiment`` block, and that block names an
id and a fidelity level. Profile resolution, parameter-policy enforcement, and
the ``MEASURED``/``MODELLED``/``ABSTRACTED``/``HYPOTHESIS`` evidence checks are
the next things to land here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.i18n import _

#: Levels of the fidelity ladder declared in the README.
FIDELITY_LEVELS = frozenset({0, 1, 2, 3, 4})


class ConfigError(Exception):
    """Raised when an experiment declaration is missing or ill-formed."""


def load_experiment(path: Path) -> dict[str, Any]:
    """Read a YAML declaration and return its validated ``experiment`` block."""
    if not path.is_file():
        raise ConfigError(_("No experiment declaration at {path}.").format(path=path))

    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ConfigError(
            _("{path} is not valid YAML: {reason}").format(path=path, reason=error)
        ) from error

    if not isinstance(document, dict):
        raise ConfigError(
            _("{path} must contain a YAML mapping at the top level.").format(path=path)
        )

    experiment = document.get("experiment")
    if not isinstance(experiment, dict):
        raise ConfigError(_("{path} is missing an 'experiment' block.").format(path=path))

    if "id" not in experiment:
        raise ConfigError(_("The 'experiment' block must declare an 'id'."))

    level = experiment.get("fidelity_level")
    if level not in FIDELITY_LEVELS:
        message = _("Unknown fidelity level {level!r}; expected one of 0, 1, 2, 3, 4.")
        raise ConfigError(message.format(level=level))

    return experiment


__all__ = ["FIDELITY_LEVELS", "ConfigError", "load_experiment"]
