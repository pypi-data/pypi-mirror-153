"""
Calculation of Global Environment Monitoring Index using the Near-Infrared and Red bands

Formula to calculate variable 'n': ( 2 * ( NIR ^2 - RED ^2) + 1.5 * NIR + 0.5 * RED ) / ( NIR + RED + 0.5 )

Formula to calculate GEMI: ( n * (1- 0.25n) ) - ( (RED - 0.125) / (1-RED) )

Wavelengths: 640nm :760nm , 780nm : 1400nm
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
    Function for calculating the GEMI
    
    Input Parameters:
        1. band_nir => NIR band of the satellite image
        2. band_red => Red band of the satellite image

    Output Parameters:
        1. gemi => GEMI for the entire satellite image
    """

    if band_nir.transform[0] != ground_sampling_distance:
        band_nir_array = reSampleBand(band_nir, ground_sampling_distance)
    else:
        band_nir_array = np.array(band_nir.read(1), dtype=np.float32)

    if band_red.transform[0] != ground_sampling_distance:
        band_red_array = reSampleBand(band_red, ground_sampling_distance)
    else:
        band_red_array = np.array(band_red.read(1), dtype=np.float32)
    
    n_var = (2*(band_nir_array**2 - band_red_array**2) + 1.5*band_nir_array + 0.5*band_red_array)/(band_nir_array + band_red_array + 0.5) 
    gemi = (n_var*(1-(0.25*n_var))) - ((band_red_array-0.125)/(1-band_red_array))

    return np.array(gemi, dtype=np.float32)
    pass
