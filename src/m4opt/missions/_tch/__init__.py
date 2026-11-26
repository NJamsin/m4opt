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
from . import data

def _buil_skygrid():
    table = Table.read(
        resources.files(data) / "TCH.tess",
        format="ascii.no_header",
        names=["field_id", "ra", "dec"],
    )
    return SkyCoord(table["ra"] * u.deg, table["dec"] * u.deg)


tch = Mission(
    name="tch",
    fov=RectangleSkyRegion(
        center=SkyCoord(0 * u.deg, 0 * u.deg), width= 1.85 * u.deg, height= 1.85 * u.deg
    ),
    constraints=(
        AirmassConstraint(2.5)
        & AltitudeConstraint(15 * u.deg, 85 * u.deg)
        & DeclinationConstraint(30 * u.deg,-90 * u.deg)
        & AtNightConstraint.twilight_astronomical()
        & MoonSeparationConstraint(30 * u.deg)
    ),
    observer_location=EarthFixedObserverLocation(
        EarthLocation.from_geodetic(
                        lon=-70.7322 * u.deg,
                        lat=-29.2608 * u.deg,
                        height=2347.0 * u.m,
                        )
    ),
    skygrid={
        "gwemopt": _buil_skygrid(),
        "sinusoidal": skygrid.sinusoidal((1.85 * u.deg)**2)
    },
    slew= EigenAxisSlew( # check the values because I am not sure they are correct
        max_angular_velocity=60 * u.deg / u.s,
        max_angular_acceleration=120 * u.deg / u.s**2,
        settling_time=5 * u.s # to include readout
    ),
    detector=Detector(
        area=np.pi * np.square(0.5 * 25 * u.cm),
        plate_scale=(3.3518 * u.arcsec) ** 2, 
        read_noise=8,                              
        dark_noise=0.0015 * u.Hz,                    
        gain=1,
        background=SkyBackground.medium() + ZodiacalBackground(),
        bandpasses={band: bandpass_from_svo(f"SLOAN/SDSS.{band}prime_filter") for band in "griz"}
    ),
)
tch.__doc__ = r"""TAROT TCH (La Palma).

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