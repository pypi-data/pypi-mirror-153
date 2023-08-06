"""
Creating a memory raster for merging. A separate file and function as it does not come under the umbrella of merging or creating a new raster profile.
"""

import numpy
import rasterio

from rasterio.io import MemoryFile

def createMemRaster(src_profile, numpy_array):
    """
    Function for creating a new profile.

    Input parameters : 
        1. src_profile => Profile to which the raster should be written
        2. numpy_array => Numpy array that has to be written to a raster file.

    Output :
        1. dataset => raster created using the src_profile and numpy_array
    """
    with MemoryFile() as memfile:
        dataset = memfile.open(**src_profile)
        dataset.write(numpy_array)
        del numpy_array
        pass

    return dataset
    pass