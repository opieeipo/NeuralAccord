"""Deterministic seeding.

A reported result carries a seed list, seed-level outcomes, and variance --
never a single best run. Seeding goes through ``SeedSequence`` so that every
independent stochastic component of a run gets its own stream from one root
seed, and so that adding a component later does not shift the streams of the
ones already there.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


def seed_manifest(seeds: Iterable[int]) -> list[int]:
    """Normalize a requested seed list: sorted, de-duplicated, non-negative."""
    unique = {int(seed) for seed in seeds}
    if any(seed < 0 for seed in unique):
        raise ValueError("Seeds must be non-negative.")
    return sorted(unique)


def spawn_generators(seed: int, names: Sequence[str]) -> dict[str, np.random.Generator]:
    """Derive one independent generator per named component from a root seed.

    Naming the streams -- rather than pulling them off a shared generator in
    call order -- is what keeps a run reproducible when the code around it
    changes.
    """
    root = np.random.SeedSequence(seed)
    children = root.spawn(len(names))
    return {name: np.random.default_rng(child) for name, child in zip(names, children, strict=True)}


__all__ = ["seed_manifest", "spawn_generators"]
