"""
Calculation of Disease Water Stres Index[DSWI] using 547nm, 682nm, 802nm, 1657nm

Formula : (802 + 547)/(1657 - 682)
Wavelengths : 547nm, 682nm, 802nm, 1657nm
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

def calculate(band_547, band_682, band_802, band_1657, ground_sampling_distance):
    """
    Function for calculating the DWSI
    
    Input Parameters:
        1. band_547 => 550nm band of the satellite image
        2. band_682 => 670nm band of the satellite image
        3. band_802 => 800nm band of the satellite image
        4. band_1657 => 1657nm band of the satellite image

    Output Parameters:
        1. dwsi => DWSI for the entire satellite image
    """

    if band_547.transform[0] != ground_sampling_distance:
        band_547_array = reSampleBand(band_547, ground_sampling_distance)
    else:
        band_547_array = np.array(band_547.read(1), dtype=np.float32)    

    if band_682.transform[0] != ground_sampling_distance:
        band_682_array = reSampleBand(band_682, ground_sampling_distance)
    else:
        band_682_array = np.array(band_682.read(1), dtype=np.float32)    

    if band_802.transform[0] != ground_sampling_distance:
        band_802_array = reSampleBand(band_802, ground_sampling_distance)
    else:
        band_802_array = np.array(band_802.read(1), dtype=np.float32)    

    if band_1657.transform[0] != ground_sampling_distance:
        band_1657_array = reSampleBand(band_1657, ground_sampling_distance)
    else:
        band_1657_array = np.array(band_1657.read(1), dtype=np.float32)

    dwsi = (band_802_array + band_547_array)/(band_1657_array - band_682_array)

    return np.array(dwsi, dtype=np.float32)
    pass
