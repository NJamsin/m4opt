"""This module contains builtin settings for supported Networks (combinations of missions)."""

from ._core import Network
from ._ground import ground
from ._tarot import tarot
from ._toy import toy

__all__ = ("Network", "ground", "tarot", "toy")