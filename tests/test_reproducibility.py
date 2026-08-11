"""Seeding is the foundation of every reportable result, so it is tested first."""

from __future__ import annotations

import numpy as np
import pytest

from core.reproducibility.seeds import seed_manifest, spawn_generators


def test_seed_manifest_sorts_and_deduplicates() -> None:
    assert seed_manifest([1044, 1042, 1042, 1043]) == [1042, 1043, 1044]


def test_seed_manifest_rejects_negative_seeds() -> None:
    with pytest.raises(ValueError):
        seed_manifest([1042, -1])


def test_same_seed_reproduces_the_same_draws() -> None:
    first = spawn_generators(1042, ["channel", "task"])
    second = spawn_generators(1042, ["channel", "task"])
    assert first["channel"].random(8).tolist() == second["channel"].random(8).tolist()


def test_named_streams_are_independent() -> None:
    generators = spawn_generators(1042, ["channel", "task"])
    channel = generators["channel"].random(64)
    task = generators["task"].random(64)
    assert not np.allclose(channel, task)


def test_adding_a_stream_does_not_shift_existing_ones() -> None:
    """A later component must not perturb an earlier one's stream."""
    before = spawn_generators(1042, ["channel", "task"])["channel"].random(8)
    after = spawn_generators(1042, ["channel", "task", "plasticity"])["channel"].random(8)
    assert before.tolist() == after.tolist()
