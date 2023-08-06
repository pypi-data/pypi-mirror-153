"""
Example for downloading one Sentinel 2 tile for a specific AOI. Currently all parameters are required to be input by the user.

This example showcases multi-processing in the download and resampling of all bands

Input parameters:
    1. geojson                  => GeoJSON for the Area of Interest[AOI]. Optional with a default value
    2. start_date               => The initial date from when data should be requested from STAC API. Format maintained is YYYY-MM-DD. Optional with a default value.
    3. end_date                 => The final date before which data should be requested from STAC API. Format maintained is YYYY-MM-DD. Optional with a default value.
    4. bands                    => The bands to be requested from the STAC API for the Sentinel 2 tiles. Comma separated list. Optional with default being ["B02","B03","B04"]
    5. ground_sampling_distance => The ground sampling distance to which all bands should be resampled to. Optional with a default value of 10m.
    6. destination_folder       => The folder location where the obtained TIF files should be stored.
    7. num_threads              => Number of processes to be run simultaneously. Defaults to number of CPUs present on the machine

Output parameters:
    Stores the data obtained in a file specified by the user.

Example UseCase : 
python download_tiles.py --geojson ../../test_aoi.geojson --start_date 2020-02-01 --end_date 2020-02-27 --bands B02,B03,B04 --ground_sampling_distance 10 --destination_folder ../../Test_Examples_Folder --num_threads 12
"""

# importing libraries
import numpy as np
import json, argparse, rasterio, os

import sys
sys.path.insert(0, "./../") # Changing the system path to root directory of the library. This is needed to actually call the Kawa Platform library

from kawaplatformlibrary.data import sentinel2dataingestion
from kawaplatformlibrary.preprocessing import splitgeojson
from kawaplatformlibrary.postprocessing.mosiac import mergeBands

from rasterio import Affine
from joblib import Parallel, delayed

# Optional arguments for the user
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--geojson", required=True, 
    help="Path to GEOJSON file containing the AOI.")
ap.add_argument("-s", "--start_date", required=True, 
    help="Start date in YYYY-MM-DD format")
ap.add_argument("-e", "--end_date", required=True, 
    help="End date in YYYY-MM-DD format")
ap.add_argument("-b", "--bands", nargs="?", default=["B02","B03","B04"],
    help="Comma separated list of bands")
ap.add_argument("-d","--ground_sampling_distance", nargs="?", default=10, type=int,
    help="Ground Sampling Distance required for each band")
# This is not optional. User should input this
ap.add_argument("-f", "--destination_folder", required=True,
    help="Path to directory for storage. Use the full OS path and not relative path")
ap.add_argument("-t", "--num_threads", nargs="?", default=os.cpu_count(), type=int,
    help="Number of processes to be run simultaneously.")
args = vars(ap.parse_args())

bands = [band.strip() for band in args["bands"].split(',')]

# Reading the GeoJSON of the AOI and extracting the coordinates json. {"type": "Polygon", "coordinates":[[[...], [...], ...]]]}
with open(args["geojson"], "r") as in_file:
    geojson_contents = json.load(in_file)
    geojson_coordinates = geojson_contents["features"][0]["geometry"]
    in_file.close()
    pass


def getBands(num_tile, split_geojson_polygon):
    """
    Obtaining the hrefs for split polygon tiles.
    """
    dataCheck = sentinel2DataIngestion.obtainData(split_geojson_polygon, args["start_date"], args["end_date"], bands)

    sentinel2_tile_data = {}

    if dataCheck[0]:
        sentinel2_tile_data = dataCheck[2]

        pass

    return sentinel2_tile_data
    pass

def downloadData(rasters_href):
    """
    Downloading and storing the data in the destination folder.
    """
    print("[INFO] Downloading data for {}".format(rasters_href["img_id"]))

    destination_file = args["destination_folder"] + rasters_href["img_id"] + ".tif"

    bands_rasters_list = []
    bands_data = rasters_href["band_data"]

    # Reading the bands into memory as numpy arrays
    for j, band in enumerate(bands_data):
        band_href = bands_data[band]["href"]
        band_src = rasterio.open(band_href)
        bands_rasters_list.append(band_src)

        # Creating the destination profile for each Sentinel 2 tile. Will be used for storing the current tile.
        if j == 0:

            band_transform = band_src.transform
            scale = band_src.transform[0] // args["ground_sampling_distance"]

            resample_transform = Affine(band_transform.a / scale, band_transform.b, band_transform.c, band_transform.d, band_transform.e / scale, band_transform.f)

            resample_width = int(band_src.height * scale)
            resample_height = int(band_src.width * scale)

            dst_profile = band_src.profile
            dst_profile.update(transform=resample_transform, driver="GTIFF", height=resample_height, width=resample_width, count=len(bands))
            pass
        pass

    # Resampling and merging the bands
    merged_resample_bands = mergeBands(bands_rasters_list, args["ground_sampling_distance"])

    # Storing the Sentinel 2 tile in the destination folder with tile name corresponding to the tile ID
    with rasterio.open(destination_file, "w", **dst_profile) as out_file:
        for i in range(merged_resample_bands.shape[0]):
            out_file.write(merged_resample_bands[i].astype(rasterio.float32), i+1)
            pass
        pass

    print("[INFO] Finished downloading data for {}".format(rasters_href["img_id"]))
    pass

geojson_split_coordinates_list = splitGeojson.split("SENTINEL2", geojson_coordinates)

print(len(geojson_split_coordinates_list))

# If num_threads specified is greater than number of CPU cores, default to number of CPU cores.
if args["num_threads"] > os.cpu_count():
    args["num_threads"] = os.cpu_count()
    pass

print("[INFO] Running with {} number of processes.".format(str(args["num_threads"])))

print("[INFO] Obtaining the hrefs for the sentinel 2 tiles present in the AOI.")
aoi_sentinel2_data = Parallel(n_jobs=args["num_threads"])(delayed(getBands)(i+1, split_geojson_polygon) for i, split_geojson_polygon in enumerate(geojson_split_coordinates_list))


print("[INFO] Starting process to download tiles.")
for sentinel2_data  in aoi_sentinel2_data:
    if sentinel2_data:
        downloadData(sentinel2_data)
        pass
    pass

print("[END] Finished downloading all Sentinel 2 tiles present in the AOI.")