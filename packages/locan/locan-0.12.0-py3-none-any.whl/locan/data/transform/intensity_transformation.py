"""

Transform localization intensities.

Localization intensities can be given in counts, electrons or photons.
Here we provide often used transformation functions.

"""
import sys

import numpy as np
import pandas as pd

from locan.data.locdata import LocData
import locan.data.hulls
from locan.data.region import Region
from locan.simulation import simulate_uniform
from locan.data.metadata_utils import _modify_meta
from locan.dependencies import HAS_DEPENDENCY



__all__ = ['transform_counts_to_photons']


def _transform_counts_to_photons(intensities: np.ndarray, offset: float, gain: float, conversion_factor: float) \
        -> np.ndarray:
    """

    Parameters
    ----------
    intensities
    offset
    gain
    conversion_factor

    Returns
    -------

    """
    return intensities