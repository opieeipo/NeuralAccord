"""The channel interface every fidelity level implements.

SILENCE and substitution are kept as *separate* observable outcomes. Collapsing
them would make erasure and interference indistinguishable in the trace, and
the Level 0 experiment sequence exists partly to tell them apart.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable

import numpy as np


class Outcome(StrEnum):
    """What happened to one transmitted symbol."""

    DELIVERED = "delivered"
    #: Observable erasure. A diagnostic control: real postsynaptic systems do
    #: not receive a labeled notice of a failed release.
    SILENCE = "silence"
    #: Effective interference, standing in for competing activity, timing
    #: jitter, and background noise.
    SUBSTITUTED = "substituted"


@dataclass(frozen=True, slots=True)
class Transmission:
    """One symbol's passage through a channel, as recorded in the trace."""

    sent: int
    received: int | None
    outcome: Outcome
    step: int
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class Channel(Protocol):
    """A bounded, stochastic, possibly state-dependent transmission path."""

    def transmit(self, symbol: int, step: int, rng: np.random.Generator) -> Transmission:
        """Carry one symbol and report what arrived."""
        ...

    def reset(self) -> None:
        """Clear any activity-dependent state between episodes."""
        ...


__all__ = ["Channel", "Outcome", "Transmission"]
