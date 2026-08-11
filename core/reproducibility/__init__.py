"""Everything a result must carry to be reportable.

Resolved configuration, seed manifest, environment capture, dataset manifests
and checksums, declared omissions, and the control conditions. See
``docs/validation.md`` for the full checklist.
"""

from core.reproducibility.seeds import seed_manifest, spawn_generators

__all__ = ["seed_manifest", "spawn_generators"]
