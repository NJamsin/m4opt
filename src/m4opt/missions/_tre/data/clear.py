import numpy as np
from astropy import units as u
from synphot import SpectralElement
from synphot.models import Empirical1D

# TARTO TRE Clear filter based on the FLI ProLine PL16803 QE curve
# see: https://homepage.physics.uiowa.edu/~pkaaret/2013f_29c137/PL16803.pdf
wavelength = np.arange(360, 1101, 20) * u.nm
qe = np.array(
    [
    0.29,0.38,0.41,0.44,0.45,0.45,0.50,0.55,0.59,0.60,  # 360–540
    0.59,0.59,0.55,0.53,0.51,0.45,0.43,0.42,0.42,0.39,  # 560–740
    0.35,0.33,0.32,0.30,0.25,0.22,0.20,0.16,0.14,0.11,  # 760–940
    0.09,0.06,0.05,0.04,0.03,0.02,0.01,0.01,  # 960–1100
    ]
)

wavelength = np.concatenate([[350], wavelength.value, [1110]]) * u.nm
qe = np.concatenate([[0], qe, [0]])

tre_clear = SpectralElement(
    Empirical1D, points=wavelength, lookup_table=qe * 0.7, fill_value=0
)