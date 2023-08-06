"""
Calculation of SAVI using the Near-Infrared and Infrared bands

Formula : ((NIR-RED)/(NIR + RED + BRIGHTNESS_CORRECTION_FACTOR)) * (1.0  + BRIGHTNESS_CORRECTION_FACTOR)
Wavelenghts : 640:760nm, 780:1400nm
"""

import numpy as np
import pandas as pd
import rasterio, argparse, os

from kawaplatformlibrary.postprocessing.mosiac import reSampleBand

def store():
    """
    This will be done when we have decided on the data storage strategy.
    """
    pass

def calculate(band_nir, band_red, ground_sampling_distance, brightness_correction_factor=0.5):
    """
    Function for calculating the SAVI
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_red => Red band of the satellite image
        3. brightness_correction_factor => 

    Output Parameters:
        1. savi => SAVI for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_red.transform[0] != ground_sampling_distance:
        band_red_array = reSampleBand(band_red, ground_sampling_distance)
    else:
        band_red_array = np.array(band_red.read(1), dtype=np.float32)

    savi = ((band_nir_array - band_red_array)/(band_nir_array + band_red_array + brightness_correction_factor)) * (1.0 + brightness_correction_factor)

    return np.array(savi, dtype=np.float32)
    pass
