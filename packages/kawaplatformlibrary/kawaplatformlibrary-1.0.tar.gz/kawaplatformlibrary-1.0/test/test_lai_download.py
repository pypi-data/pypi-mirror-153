# importing libraries
import numpy as np
import json, argparse, rasterio, os

import sys
sys.path.insert(1, "./../")

from kawaplatformlibrary.data import sentinel2dataingestion
from kawaplatformlibrary.data.preprocessing import splitgeojson
from kawaplatformlibrary.postprocessing.mosiac import mergeBands
from kawaplatformlibrary.postprocessing.createprofile import createNewProfile

from kawaplatformlibrary.indices import lai

from rasterio import Affine

ap = argparse.ArgumentParser()
ap.add_argument("-g", "--geojson", required=True, 
    help="Path to GEOJSON file containing the AOI.")
ap.add_argument("-s", "--start_date", required=True, 
    help="Start date in YYYY-MM-DD format")
ap.add_argument("-e", "--end_date", required=True, 
    help="End date in YYYY-MM-DD format")
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

user_bands = ["B02", "B04", "B08"]

# Reading the GeoJSON of the AOI and extracting the coordinates json. {"type": "Polygon", "coordinates":[[[...], [...], ...]]]}
with open(args["geojson"], "r") as in_file:
    geojson_contents = json.load(in_file)
    geojson_coordinates = geojson_contents["features"][0]["geometry"]
    in_file.close()
    pass

# Obtaining image url from STAC API. dataCheck = [0/1, "[ERROR]/["INFO"]", [{}/{<data>}, tile_number]]
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
    
    band_blue = rasterio.open(bands_data["B02"]["href"])
    band_red  = rasterio.open(bands_data["B04"]["href"])
    band_nir  = rasterio.open(bands_data["B08"]["href"])

    band_lai = lai.calculate(band_nir, band_red, band_blue, args["ground_sampling_distance"])

    dst_profile = createNewProfile(bands_blue.transform, bands_blue.profile, ground_sampling_distance=10, num_bands=1)

    # Storing the Sentinel 2 tile in the destination folder with tile name corresponding to the tile ID
    with rasterio.open(destination_file, "w", **dst_profile) as out_file:
            out_file.write(band_lai.astype(rasterio.float32), 1)
            pass
        pass

    print("[INFO] Finished creating LAI data for {}".format(rasters_href["img_id"]))
    pass

for sentinel2_data in sentinel2_data_aoi:
    dataCheck = sentinel2_data[0]
    if dataCheck == 1:
        downloadData(sentinel2_data[2][1])
    else:
        print("[INFO] No images found for tile number {}".format(sentinel2_data[2][0]))
        print(sentinel2_data[1])
    pass