"""
Calculation of Normalised Difference Water Index (Surface Water) using Near Infrared and Green bands

Formula : (NIR - GREEN) / (NIR + GREEN)

Wavelengths : 490nm: 570nm, 780nm :1400nm
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

def calculate(band_nir, band_green, ground_sampling_distance):
    """
    Function for calculating the NDWI (Surface water)
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_green => Green band of the satellite image

    Output Parameters:
        1. ndwi_sw => NDWI (Surface water) for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_green.transform[0] != ground_sampling_distance:
        band_green_array = reSampleBand(band_green, ground_sampling_distance)
    else:
        band_green_array = np.array(band_green.read(1), dtype=np.float32)

    ndwi_sw = (band_green_array - band_nir_array)/(band_green_array + band_nir_array)

    return np.array(ndwi_sw, dtype=np.float32)
    pass
