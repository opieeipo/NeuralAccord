"""The experiment declarations shipped in ``configs/`` must stay loadable."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.config import ConfigError, load_experiment

REPO_ROOT = Path(__file__).resolve().parent.parent

SHIPPED_CONFIGS = [
    REPO_ROOT / "configs" / "mouse" / "v1_l23_dynamic_synapse.yaml",
    REPO_ROOT / "configs" / "bci" / "cursor_cross_session.yaml",
]


@pytest.mark.parametrize("path", SHIPPED_CONFIGS, ids=lambda p: p.name)
def test_shipped_configs_load(path: Path) -> None:
    experiment = load_experiment(path)
    assert experiment["id"]
    assert experiment["fidelity_level"] in {0, 1, 2, 3, 4}


def test_missing_file_is_a_config_error(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        load_experiment(tmp_path / "absent.yaml")


def test_missing_experiment_block_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "no_block.yaml"
    path.write_text("biology:\n  species: mouse\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_experiment(path)


def test_unknown_fidelity_level_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "off_ladder.yaml"
    path.write_text("experiment:\n  id: x\n  fidelity_level: 9\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_experiment(path)
