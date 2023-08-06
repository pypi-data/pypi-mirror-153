"""

NOTE: Run this code outside of the kawaplatformlibrary. Basically move this code to right outside the kawaplatformlibrary and then run this code.

"""

"""
Example for downloading one Sentinel 2 tile for a specific AOI. All parameters are optional and contain default values which will be used for downloading the Sentinel 2 tile. The only parameter which is required is the destination file for storing the TIF obtained from STAC API.s

Input parameters:
    1. geojson                  => GeoJSON for the Area of Interest[AOI]. Optional with a default value
    2. start_date               => The initial date from when data should be requested from STAC API. Format maintained is YYYY-MM-DD. Optional with a default value.
    3. end_date                 => The final date before which data should be requested from STAC API. Format maintained is YYYY-MM-DD. Optional with a default value.
    4. bands                    => The bands to be requested from the STAC API for the Sentinel 2 tiles. Comma separated list. Optional with default being ["B02","B03","B04"]
    5. ground_sampling_distance => The ground sampling distance to which all bands should be resampled to. Optional with a default value of 10m.
    6. destination_file         => The file location where the obtained TIF file should be stored.

Output parameters:
    Stores the data obtained in a file specified by the user.

Example UseCase : 
python test_download_tiles.py --geojson ../../test_aoi.geojson --start_date 2020-02-01 --end_date 2020-02-27 --bands B02,B03,B04 --ground_sampling_distance 10 --destination_folder ../../Test_Examples_File_Path.tif --num_threads 6
"""

# importing libraries
import numpy as np
import json, argparse, rasterio, os

import sys
sys.path.insert(1, "./../") # Changing the system path to root directory of the library. This is needed to actually call the Kawa Platform library

from kawaplatformlibrary.data import sentinel2dataingestion
from kawaplatformlibrary.data.preprocessing import splitgeojson
from kawaplatformlibrary.postprocessing.mosiac import mergeBands
from kawaplatformlibrary.postprocessing.createprofile import createNewProfile

from rasterio import Affine

# Optional arguments for the user
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--geojson", nargs="?", default="", 
    help="Path to GEOJSON file containing the AOI.")
ap.add_argument("-s", "--start_date", required=True, 
    help="Start date in YYYY-MM-DD format")
ap.add_argument("-e", "--end_date", required=True, 
    help="End date in YYYY-MM-DD format")
ap.add_argument("-b", "--bands", required=True,
    help="Comma separated list of bands")
ap.add_argument("-t", "--tci", nargs="?", default=False, type=bool,
    help="If True Colour Image is required.")
ap.add_argument("-d","--ground_sampling_distance", nargs="?", default=10, type=int,
    help="Ground Sampling Distance required for each band")
# This is not optional. User should input this
ap.add_argument("-f", "--destination_folder", required=True,
    help="Path to file for storage. Use the full OS path and not relative path")
ap.add_argument("-n", "--num_threads", required=True, type=int,
    help="Number of parallel process to run.")
args = vars(ap.parse_args())

user_bands = [band.strip() for band in args["bands"].split(',')]

# Reading the GeoJSON of the AOI and extracting the coordinates json. {"type": "Polygon", "coordinates":[[[...], [...], ...]]]}
with open(args["geojson"], "r") as in_file:
    geojson_contents = json.load(in_file)
    geojson_coordinates = geojson_contents["features"][0]["geometry"]
    in_file.close()
    pass

# Obtaining image url from STAC API. dataCheck = [0/1, "[ERROR]/["INFO"]", {}/{<data>}]
print("[INFO] Obtianing data for the AOI")
sentinel2_data_class_obtain_data = sentinel2dataingestion.ObtainData(aoi_geojson=geojson_coordinates, start_date=args['start_date'], end_date=args["end_date"], bands=user_bands, TCI=args["tci"], cloud_cover=10)
sentinel2_data_aoi = sentinel2_data_class_obtain_data.getData(num_threads = args["num_threads"])
print("[INFO] Finished finding data for the AOI.")

def downloadData(rasters_href):
    """
    Downloading and storing the data in the destination folder.
    """
    print("[INFO] Downloading data for {}".format(rasters_href["img_id"]))

    destination_file = rasters_href["img_id"] + ".tif"
    destination_file = os.path.join(args["destination_folder"], destination_file)

    bands_rasters_list = []
    bands_data = rasters_href["band_data"]

    # Reading the bands into memory as numpy arrays
    for j, band in enumerate(bands_data):

        band_href = bands_data[band]["href"]
        band_src = rasterio.open(band_href)
        bands_rasters_list.append(band_src)

        # Creating the destination profile for each Sentinel 2 tile. Will be used for storing the current tile.
        if j == 0:
            num_bands = len(user_bands)
            dst_profile = createNewProfile(band_src.transform, band_src.profile, ground_sampling_distance=10, num_bands=num_bands)
            pass
        pass

    # Resampling and merging the bands
    merged_resample_bands = mergeBands(bands_rasters_list, args["ground_sampling_distance"])
    print("[INFO] Finished merging bands for img : {}".format(rasters_href["img_id"]))

    if args["tci"]:

        bands_tci_href = rasters_href["TCI"]
        bands_tci_src  = rasterio.open(bands_tci_href)
        bands_tci_data = bands_tci_src.read()

        destination_file_tci = args["destination_folder"] + rasters_href["img_id"] + "_TCI.tif"

        tci_profile = bands_tci_src.profile

        print("[INFO] Storing TCI image for img : {}".format(rasters_href["img_id"]))
        with rasterio.open(destination_file_tci, "w", **tci_profile) as out_file_tci:
            out_file_tci.write(bands_tci_data[0], 1)
            out_file_tci.write(bands_tci_data[1], 2)
            out_file_tci.write(bands_tci_data[2], 3)
            pass 
        print("[INFO] Finished storing TCI image for img : {}".format(rasters_href["img_id"]))
        pass

    # Storing the Sentinel 2 tile in the destination folder with tile name corresponding to the tile ID
    with rasterio.open(destination_file, "w", **dst_profile) as out_file:
        for i in range(merged_resample_bands.shape[0]):
            out_file.write(merged_resample_bands[i].astype(rasterio.float32), i+1)
            pass
        pass

    print("[INFO] Finished downloading data for {}".format(rasters_href["img_id"]))
    pass

for sentinel2_data in sentinel2_data_aoi:
    dataCheck = sentinel2_data[0]
    if dataCheck == 1:
        downloadData(sentinel2_data[2][1])
    else:
        print("[INFO] No images found for tile number {}".format(sentinel2_data[2][0]))
        print(sentinel2_data[1])
    pass