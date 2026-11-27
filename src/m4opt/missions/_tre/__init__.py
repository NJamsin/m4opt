from importlib import resources

import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord
from astropy.table import Table
from regions import RectangleSkyRegion

from ... import skygrid
from ...constraints import (
    AirmassConstraint,
    AltitudeConstraint,
    AtNightConstraint,
    MoonSeparationConstraint,
    DeclinationConstraint,
)
from ...dynamics import EigenAxisSlew
from ...observer import EarthFixedObserverLocation
from ...synphot import Detector, bandpass_from_svo
from ...synphot.background import SkyBackground, ZodiacalBackground
from .._core import Mission
from .data.clear import tre_clear
from . import data


def _buil_skygrid():
    table = Table.read(
        resources.files(data) / "TRE.tess",
        format="ascii.no_header",
        names=["field_id", "ra", "dec"],
    )
    return SkyCoord(table["ra"] * u.deg, table["dec"] * u.deg)


tre = Mission(
    name="tre",
    fov=RectangleSkyRegion(
        center=SkyCoord(0 * u.deg, 0 * u.deg), width=4.15 * u.deg, height=4.15 * u.deg
    ),
    constraints=(
        AirmassConstraint(2.5)
        & AltitudeConstraint(20 * u.deg, 85 * u.deg)
        & DeclinationConstraint(40 * u.deg, -90 * u.deg)
        & AtNightConstraint.twilight_astronomical()
        & MoonSeparationConstraint(30 * u.deg)
    ),
    observer_location=EarthFixedObserverLocation(
        EarthLocation.from_geodetic(
            lon=55.407463 * u.deg,
            lat=-21.201387 * u.deg,
            height=970.0 * u.m,
        )
    ),
    skygrid={
        "gwemopt": _buil_skygrid(),
        "sinusoidal": skygrid.sinusoidal((4.15 * u.deg) ** 2),
    },
    slew=EigenAxisSlew(  # check the values because I am not sure they are correct
        max_angular_velocity=60 * u.deg / u.s,
        max_angular_acceleration=120 * u.deg / u.s**2,
        settling_time=10 * u.s,  # to include readout
    ),
    detector=Detector(
        area=np.pi * np.square(0.5 * 18 * u.cm),
        plate_scale=(3.7128 * u.arcsec) ** 2,
        read_noise=11,
        dark_noise=0.05 * u.Hz,
        gain=1,
        background=SkyBackground.high() + ZodiacalBackground(),
        bandpasses={"tre_clear": tre_clear},
    ),
)
tre.__doc__ = r"""TAROT TRE (Réunion).

TAROT (Télescope à action rapide pour les objets transitoires) 
is an automated telescope network located at different sites around 
the world with automated observations (without human interaction):footcite:`https://grandma.ijclab.in2p3.fr/observatories/tarot/`. 

Note
----
Telescope and detector parameters are from
`Boër et al. (2017) <https://conference.sdo.esoc.esa.int/proceedings/sdc7/paper/382>`_.

References
----------
.. footbibliography::
"""
