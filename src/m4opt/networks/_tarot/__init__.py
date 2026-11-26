from .._core import Network
from ...missions import tre, tca, tch

tarot = Network(
    name="tarot",
    telescopes=[tre, tca, tch],
)
tarot.__doc__ = r"""TAROT (Télescope à action rapide pour les objets transitoires).
TAROT is an automated telescope network located at different sites around 
the world with automated observations (without human interaction):footcite:`https://grandma.ijclab.in2p3.fr/observatories/tarot/`. 
"""