"""The CLI must fail honestly rather than produce numbers it cannot justify."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.cli import main

REPO_ROOT = Path(__file__).resolve().parent.parent
MOUSE_CONFIG = REPO_ROOT / "configs" / "mouse" / "v1_l23_dynamic_synapse.yaml"


def test_run_reports_not_implemented_rather_than_faking_a_result(
    capsys: pytest.CaptureFixture[str],
) -> None:
    status = main(["run", str(MOUSE_CONFIG), "--seed", "1042"])
    assert status == 3
    captured = capsys.readouterr()
    assert "not implemented" in captured.err.lower()


def test_bad_config_exits_with_a_distinct_status(tmp_path: Path) -> None:
    assert main(["bci-evaluate", str(tmp_path / "absent.yaml")]) == 2


def test_lang_option_is_accepted(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--lang", "fr", "run", str(MOUSE_CONFIG), "--seed", "1042"]) == 3
    assert capsys.readouterr().out


def test_seed_option_repeats_into_a_list(capsys: pytest.CaptureFixture[str]) -> None:
    main(["run", str(MOUSE_CONFIG), "--seed", "1042", "--seed", "1043"])
    assert "2" in capsys.readouterr().out
