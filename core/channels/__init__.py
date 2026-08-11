"""Transmission models: what survives the trip between two systems.

A channel abstracts effective transmission, not anatomy. A token is not a
vesicle and a channel is not a network socket; see
``docs/abstraction-boundaries.md`` for what each model retains and omits.

Level 0 channels apply a fixed erasure and interference rate. Level 1 replaces
them with activity-dependent release, facilitation, depression, and delay drawn
from a named evidence profile.
"""

from core.channels.base import Channel, Transmission

__all__ = ["Channel", "Transmission"]
