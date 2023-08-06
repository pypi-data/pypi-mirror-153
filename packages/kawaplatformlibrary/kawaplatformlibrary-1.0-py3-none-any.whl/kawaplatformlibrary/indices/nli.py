"""
Calculation of Non Linear Index using the NIR and Red bands.

Formula : (NIR*NIR - RED) / (NIR*NIR + RED)
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

def calculate(band_nir, band_red, ground_sampling_distance):
    """
    Function for calculating the NLI
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_red => Red band of the satellite image

    Output Parameters:
        1. nli => NLI for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_red.transform[0] != ground_sampling_distance:
        band_red_array = reSampleBand(band_red, ground_sampling_distance)
    else:
        band_red_array = np.array(band_red.read(1), dtype=np.float32)

    nli = (np.square(band_nir_array) - band_red_array)/(np.square(band_nir_array) + band_red_array)

    return np.array(nli, dtype=np.float32)
    pass