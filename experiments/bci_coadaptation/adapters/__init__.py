"""Dataset adapters, prioritizing NWB where possible.

An adapter's only job is to produce a normalized ``BCISession`` without
laundering the data's access terms. Controlled human data are never
redistributed outside their governing data-use agreement; adapters read from a
local path the user is already permitted to hold.
"""

from experiments.bci_coadaptation.adapters.session import BCISession

__all__ = ["BCISession"]
