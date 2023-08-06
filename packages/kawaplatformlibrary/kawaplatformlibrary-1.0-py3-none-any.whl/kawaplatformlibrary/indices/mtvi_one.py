"""
Calculation of Modified Triangular Vegetation Index 1[MTVI_1] using the 800nm, 550nm and 670nm bands

Formula : 1.2 * (1.2 * (800nm - 550nm) - 2.5 * (670nm - 550nm))
Wavelengths : 550nm, 670nm, 800nm
"""

import numpy as np
import pandas as pd
import rasterio, os

from kawaplatformlibrary.postprocessing.mosiac import reSampleBand

def store():
    """
    This will be done when we have decided on the data storage strategy.
    """
    pass

def calculate(band_550, band_670, band_800, ground_sampling_distance):
    """
    Function for calculating the CIGreen
    
    Input Parameters:
        1. band_550 => 550nm band of the satellite image
        2. band_670 => 670nm band of the satellite image
        3. band_800 => 800nm band of the satellite image

    Output Parameters:
        1. mtvi_one => MTVI_1 for the entire satellite image
    """

    if band_550.transform[0] != ground_sampling_distance:
        band_550_array = np.where(band_550_array == band_550.meta["nodata"], np.NaN, band_550_array)
    else:
        band_550_array = np.array(band_550,read(1), dtype=np.float32)

    if band_670.transform[0] != ground_sampling_distance:
        band_670_array = reSampleBand(band_670, ground_sampling_distance)
    else:
        band_670_array = np.array(band_670.read(1), dtype=np.float32)

    if band_800.transform[0] != ground_sampling_distance:
        band_800_array = reSampleBand(band_800, ground_sampling_distance)
    else:
        band_800_array = np.array(band_800.read(1), dtype=np.float32)

    mtvi_one = 1.2 * (1.2*(band_800_array - band_550_array) - 2.5*(band_670_array - band_550_array))

    return np.array(mtvi_one, dtype=np.float32)
    pass
