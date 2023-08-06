"""
Function for Resampling bands, merging bands into one numpy array with a common ground sampling distance and merging a list of rasters to create one merged raster.
"""

import numpy as np
import rasterio 

from rasterio.warp import reproject, Resampling
from rasterio import transform
from rasterio.merge import merge
from rasterio import Affine

from .creatememoryraster import createMemRaster

def reSampleBand(band_raster, ground_sampling_distance):
    """
    Function for resampling the bands to a common resolution
    """

    scale = band_raster.transform[0] // ground_sampling_distance

    org_transform = band_raster.transform
    resample_transform = Affine(org_transform.a / scale, org_transform.b, org_transform.c, org_transform.d, org_transform.e / scale, org_transform.f)

    resample_height = int(band_raster.height * scale)
    resample_width = int(band_raster.width * scale)

    data = band_raster.read( # Note changed order of indexes, arrays are band, row, col order not row, col, band
            out_shape=(resample_height, resample_width),
            resampling=Resampling.cubic)

    return np.array(data[0], dtype=np.float32)
    pass

def mergeBands(list_bands_rasters, ground_sampling_distance):
    """
    Function for merging the bands into one numpy array
    """

    for i in range(len(list_bands_rasters)):
        if int(list_bands_rasters[i].transform[0]) != ground_sampling_distance:
            
            list_bands_rasters[i] = reSampleBand(list_bands_rasters[i], ground_sampling_distance)
        else:
            list_bands_rasters[i] = np.array(list_bands_rasters[i].read(1), dtype=np.float32)
        pass

    merged_bands = np.stack(list_bands_rasters)
    return merged_bands
    pass

def createMosiacTiles(list_rasters):
    """
    Function for creating the mosiac of all tiles. It currently takes all rasters and gives the transformation matrix of the mergerd rasters and an array of all the merged rasters.

    Input Parameters:
        1. list_rasters => list of rasters which have to be merged.

    Ouptut:
        1. Merged raster of all the listed rasters. 
    """

    merged_rasters_array, merged_rasters_trans = merge(list_rasters)

    merged_rasters_array_height, merged_rasters_array_width = merged_rasters_array.shape[1], merged_rasters_array.shape[2]

    dst_profile = list_rasters[0].profile

    merged_rasters_profile = dst_profile
    merged_rasters_profile.update(transform=merged_rasters_trans, driver="GTIFF", height=merged_rasters_array_height,
        width=merged_rasters_array_width)

    return createMemRaster(merged_rasters_profile, merged_rasters_array)
    pass