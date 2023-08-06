"""
Calculation of Canopy Chlorophyll Content Index using the Near-Infrared, Red and Red-Edge bands

Formula: ((NIR - RED_EDGE) / (NIR + RED_EDGE)) / ((NIR - RED) / (NIR - RED))

Wavelengths: 690nm :730nm , 780nm :1400nm
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

def calculate(band_nir, band_red, band_red_edge, ground_sampling_distance):
    """
    Function for calculating the CCCI
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_red => Red band of the satellite image
        3. band_red_edge => Red-edge band of the satellite image
    Output Parameters:
        1. ccci => CCCI for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_red.transform[0] != ground_sampling_distance:
        band_red_array = reSampleBand(band_red, ground_sampling_distance)
    else:
        band_red_array = np.array(band_red.read(1), dtype=np.float32)

    if band_red_edge.transform[0] != ground_sampling_distance:
        band_red_edge_array = reSampleBand(band_red_edge, ground_sampling_distance)
    else:
        band_red_edge_array = np.array(band_red_edge.read(1), dtype=np.float32)

    ccci = ((band_nir_array-band_red_edge_array)/(band_nir_array+band_red_edge_array))/((band_nir_array-band_red_array)/(band_nir_array-band_red_array))

    return np.array(ccci, dtype=np.float32)
    pass
