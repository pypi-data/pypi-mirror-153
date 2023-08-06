"""
Calculation of Normalised Difference Water Index (Crop Water) using Near Infrared and Short Wave Infrared bands

Formula : (NIR - SWIR) / (NIR + SWIR)

Wavelengths : 780nm :1400nm , 1400nm :3000nm
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

def calculate(band_nir, band_swir, ground_sampling_distance):
    """
    Function for calculating the NDWI (crop water)
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_swir => SWIR band of the satellite image

    Output Parameters:
        1. ndwi_cw => NDWI (crop water) for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_swir.transform[0] != ground_sampling_distance:
        band_swir_array = reSampleBand(band_swir, ground_sampling_distance)
    else:
        band_swir_array = np.array(band_swir.read(1), dtype=np.float32)


    ndwi_cw = (band_nir_array - band_swir_array)/(band_nir_array + band_swir_array)

    return np.array(ndwi_cw, dtype=np.float32)
    pass
