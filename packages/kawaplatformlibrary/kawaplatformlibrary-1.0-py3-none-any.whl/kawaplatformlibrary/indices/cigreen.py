"""
Calculation of Chlorophyll Index Green[CIGreen] using the Near-Infrared and Green bands

Formula : (NIR/GREEN) - 1
Wavelenghts : 490:570, 780:1400
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
    Function for calculating the CIGreen
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_green => Green band of the satellite image

    Output Parameters:
        1. cigreen => CIGreen for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_green.transform[0] != ground_sampling_distance:
        band_green_array = reSampleBand(band_green, ground_sampling_distance)
    else:
        band_green_array = np.array(band_green.read(1), dtype=np.float32)

    cigreen = (band_nir_array - band_green_array)/(band_nir_array + band_green_array)

    return np.array(cigreen, dtype=np.float32)
    pass
