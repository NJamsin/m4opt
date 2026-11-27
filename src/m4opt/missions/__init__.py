"""This module contains builtin settings for supported missions."""

from ._core import Mission
from ._rubin import rubin
from ._ultrasat import ultrasat
from ._uvex import uvex, uvex_downlink_orientation, uvex_lss_fov
from ._ztf import ztf
from ._tca import tca
from ._tch import tch
from ._tre import tre

__all__ = (
    "Mission",
    "rubin",
    "ultrasat",
    "uvex",
    "uvex_downlink_orientation",
    "uvex_lss_fov",
    "ztf",
    "tca",
    "tch",
    "tre",
)
