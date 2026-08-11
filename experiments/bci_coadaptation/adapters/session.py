"""The normalized ``BCISession`` data contract.

Every adapter, preprocessing step, baseline, and report in this track speaks
this structure and nothing else. Fields an adapter cannot supply are ``None``
rather than imputed: a missing recording-quality annotation is a documented
gap, not a default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True, slots=True)
class BCISession:
    """One recording session, normalized across datasets.

    Attributes:
        subject_id: Stable identifier within the source dataset.
        session_id: Session identifier; ordering across sessions must be
            recoverable, because splits are strictly chronological.
        task_type: e.g. ``"cursor_2d"``.
        neural_features: ``(n_samples, n_channels)`` threshold crossings or
            spike rates.
        timestamps: ``(n_samples,)`` seconds from session start.
        intended_kinematics: ``(n_samples, n_dims)`` where the task defines it.
        decoder_outputs: What the session's own decoder produced, when the
            recording was closed-loop.
        feedback_events: Discrete events the user saw.
        channel_metadata: Per-channel provenance, including known-bad channels.
        recording_quality: Declared quality annotations; never inferred.
        trial_labels: Trial-level supervision, used against a label budget.
        session_conditions: Anything that changed between sessions.
    """

    subject_id: str
    session_id: str
    task_type: str
    neural_features: np.ndarray
    timestamps: np.ndarray
    intended_kinematics: np.ndarray | None = None
    decoder_outputs: np.ndarray | None = None
    feedback_events: list[dict[str, Any]] = field(default_factory=list)
    channel_metadata: list[dict[str, Any]] = field(default_factory=list)
    recording_quality: dict[str, Any] = field(default_factory=dict)
    trial_labels: np.ndarray | None = None
    session_conditions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.neural_features.ndim != 2:
            raise ValueError("neural_features must be (n_samples, n_channels).")
        if self.timestamps.shape[0] != self.neural_features.shape[0]:
            raise ValueError("timestamps and neural_features must agree on n_samples.")

    @property
    def n_samples(self) -> int:
        """Number of samples in the session."""
        return int(self.neural_features.shape[0])

    @property
    def n_channels(self) -> int:
        """Number of recording channels."""
        return int(self.neural_features.shape[1])


__all__ = ["BCISession"]
