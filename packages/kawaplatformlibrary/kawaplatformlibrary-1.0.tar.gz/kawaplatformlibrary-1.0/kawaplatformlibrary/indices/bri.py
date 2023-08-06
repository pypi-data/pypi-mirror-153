"""
Calculation of Browning Reflectance Index using the 550nm, 700nm and NIR bands

Formula: ((1/550 nm) - (1/700 nm)) / (NIR)

Wavelengths: 550nm ,700nm ,780nm :1400nm
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

def calculate(band_nir, band_550, band_700, ground_sampling_distance):
    """
    Function for calculating the BRI
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_550 => 550nm spectral band of the satellite image
        3. band_700 => 700nm spectral band of the satellite image
    Output Parameters:
        1. bri => BRI for the entire satellite image
    """


    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_550.transform[0] != ground_sampling_distance:
        band_550_array = reSampleBand(band_550, ground_sampling_distance)
    else:
        band_550_array = np.array(band_550.read(1), dtype=np.float32)

    if band_700.transform[0] != ground_sampling_distance:
        band_700_array = reSampleBand(band_700, ground_sampling_distance)
    else:
        band_700_array = np.array(band_700.read(1), dtype=np.float32)

    bri = ((1/band_550_array)-(1/band_700_array))/band_nir_array

    return np.array(bri, dtype=np.float32)
    pass
