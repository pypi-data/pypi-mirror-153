"""
Creation of a data ingestion pipeline for Sentinel 2 Level 2 A data from AWS S3 bucket using STAC api.

Calls CustomExceptions to raise errors with user input data.
"""

import datetime
import os

from shapely.geometry import shape
from rasterio import Affine

from kawaplatformlibrary.data.preprocessing import splitgeojson
from kawaplatformlibrary.data.preprocessing import splitdates
from joblib import Parallel, delayed

class ObtainData():
    """
    Class for obtaining data from Sentinel 2 STAC API
    """

    def __init__(self, bands=["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B11", "B12", "B8A"], cloud_cover=5, area_coverage=90, intersection_area=20, TCI=False):
        """
        Input Parameters:
            1. bands             => List of bands from the Sentinel 2 iamge. B10 is not included in L2A
            2. cloud_cover       => Maximum cloud cover for the Sentinel 2 image
            3. area_coverage     => Minimum amount of data to be present in the image
            4. intersection_area => Minumum intersection between Bounding Box of Sentinel 2 tile and query geojson
            5. TCI               => If the True Colour Image is required or not.
        """

        self.bands             = bands
        self.cloud_cover       = cloud_cover
        self.area_coverage     = area_coverage
        self.intersection_area = intersection_area
        self.TCI               = TCI
        pass

    def getData(self, aoi_geojson, start_date, end_date, days_frequency=None, num_threads=None):
        """
        Getting the bands and their data from Sentinel 2 STAC API using multiprocessing.

        Input Parameters:
            1. aoi_geojson    => The AOI for which Sentinel 2 data is to be obtained
            2. start_date     => Starting date for inference period
            3. end_date       => Ending date for inference period
            4. days_frequenct => Frequency of intervals or frequency of Boromir drinking water instead of beer.
            4. num_threads    => Number of processes to run paralelly to obtain the data from S2 STAC API.
            
        Output:
            1. Returns a dictionary with key being the date and value being the bands data, code, and message.
            [NOTE] If days_frquency is provided, this function will yield values and not return values.
        References:
            1. ObtianData.getBandData()
        """

        # If num_threads is None or is more than the numebr of threads present on the CPU, the code uses the maximum number of threads available on the system
        if num_threads == None or num_threads > os.cpu_count():
            num_threads = os.cpu_count()
            pass

        # If days_frequency is less than 5, setting the frequency to 5 which is the temporal resolution of the satellite.
        if days_frequency < 5:
            days_frequency = 5

        # Splitting the larger GeoJSON into smaller GeoJSON.
        split_geojson_coords_list = splitgeojson.split("SENTINEL2", aoi_geojson)

        if days_frequency:
            for start_date_freq, end_date_freq in splitdates.dateGenerator(start_date, end_date, days_frequency):
                    yield Parallel(n_jobs=num_threads)(delayed(self.getBandData)(split_geojson_polygon, start_date_freq,end_date_freq, i+1) for i,split_geojson_polygon in enumerate(split_geojson_coords_list))
                pass
        else:
            return Parallel(n_jobs=num_threads)(delayed(self.getBandData)(split_geojson_polygon, start_date, end_date, i+1) for i, split_geojson_polygon in enumerate(split_geojson_coords_list))

        pass

    def getBandData(self, geojson, start_date, end_date, tile_number = 1):
        """
        Function for obtaining metadata from Sentinel 2 AWS bucket for the specific AOI 
        
        The output is a list of 3 elements. The first element is a number specifying whether the call worked or not. The second element is a text message explaining the first element. The third element is the data to be used by the user.
        
        Error messages will be numbered evens while info messages will be numbered in odd.

        Input Parameters:
            1. geojson     => The AOI for which Sentinel 2 data should be found
            2. tile_number => The tile number from split_geojson. Defaults to one.

        Output:
             Info message stating that data has been found or there is an error with the third element either being the tile_number[ERROR] or a dictionary containing the following[DATA FOUND]:
                2.1. img_id        => Sentinel 2 image ID
                2.2. band_date     => Dictionary if the user specified bands, each band is a dictionary containing the URL and Affine transform for that band.
                2.3. "init : EPSG" => The CRS for that AOI, corresponds to different UTM zones.
                2.4. bbox          => Bounding box of the Sentinel 2 tile. May not correspond to the actual tile.
                2.5. sensing_date  => The date when the data was obtained in miliseconds since epoch
                2.6. TCI           => If TCI is specified by the user, it will be added otherwise it is not.
        
        Called:
            1. ObtainData.getBandData()

        ERROR Codes:
            1. 0 =>  Band specified by user is not present in Sentinel 2 STAC API.
            2. 2 =>  GeoJSON type is not a Polygon
            3. 4 =>  URL could not be accessed due to errorneous user input
            4. 6 =>  No images could be found
        
        INFO Codes
            1. 1 => Images found and links sent as a dictionary
        """

        # Default list of bands for checking user inputted bands
        default_bands = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B11", "B12", "B8A"] 

        # Checking if bands given are correct or not. Error passed when user inputed band is incorrect as per default_bands list
        for user_band in self.bands:
            if user_band not in default_bands:
                return {start_date : [0, "[ERROR] Band is not present in Sentinel 2 Level 2A, User band: {}".format(user_band), tile_number]}
                pass
            pass

        # Reading the contents of the GeoJSON and extracting the coordinates
        # Removed reading file as it's redundant
        
        bounding_box_type = geojson["type"]
        
        # Checking the geometry type of the bounding box. Geometry type should be Polygon
        if bounding_box_type != "Polygon":
            return {start_date : [2, "[ERROR] Required GeoJSON type to be a Polygon.", tile_number]}
            pass

        bounding_box = [str(coord) for coord in shape(geojson).bounds]
        bounding_box = ",".join(bounding_box)

        shape_aoi = shape(geojson)

        url = f"https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items?limit=100&bbox=[{bounding_box[:-1]}]&datetime={start_date}T00:00:00Z/{end_date}T23:59:59Z"

        try:
            search_response = requests.get(url).json()
        except:
            return {start_date : [4, "[ERROR] URL could not be accessed", tile_number]}
            pass

        items = search_response['features']

        img_list = []

        # Taking starting date as the minimum date
        min_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        min_datetime = min_datetime.timestamp()

        for item in items:

            shape_item = shape(item["geometry"])

            # If the intersection of the Sentinel 2 tile with the current AOI is less than 30% then skip the tile.
            if (shape_aoi.intersection(shape_item).area/shape_aoi.area)*100 < self.intersection_area:
                continue
                pass

            if item['properties']["eo:cloud_cover"] < self.cloud_cover:
                
                # Two if statements to accept the different data_coverage keys as per STAC API.

                if "data_coverage" in item['properties'] and item['properties']['data_coverage'] > self.area_coverage:
                    
                    # Storing the band href link and transform in a dictionary
                    band_data = {band:{'href':item["assets"][band]["href"], 'affine_transform':Affine(*item["assets"][band]["proj:transform"][:6])} for band in item["assets"] if band in self.bands}
                    
                    # Storing the EPSG in crs format as well as a tuple of the bounding box
                    epsg_data = {"init" : "EPSG:" + str(item["properties"]["proj:epsg"])}
                    bbox = tuple(item["bbox"])
                    
                    date_sensing = item["properties"]["datetime"].split("T")[0]
                    date_sensing = datetime.datetime.strptime(date_sensing, "%Y-%m-%d")
                    date_sensing = date_sensing.timestamp() # converting the datetime string into seconds since epoch

                    # Storing it as per the unique Sentinel 2 ID. If TCI is asked, TCI is added to the dictionary separately.
                    if self.TCI:
                        img_list.append({"img_id" : item['id'], "band_data" : band_data, "init" : "EPSG:" + str(item["properties"]["proj:epsg"]), "bbox" : bbox, "sensing_date" : date_sensing, "TCI" : item["assets"]["visual"]["href"]})
                    else:
                        img_list.append({"img_id" : item['id'], "band_data" : band_data, "init" : "EPSG:" + str(item["properties"]["proj:epsg"]), "bbox" : bbox, "sensing_date" : date_sensing})
                    pass

                if "sentinel:data_coverage" in item['properties'] and item['properties']['sentinel:data_coverage'] > self.area_coverage:    

                    # Storing the band href link and transform in a dictionary
                    band_data = {band:{'href':item["assets"][band]["href"], 'affine_transform':Affine(*item["assets"][band]["proj:transform"][:6])} for band in item["assets"] if band in self.bands}
                    
                    # Storing the EPSG in crs format as well as a tuple of the bounding box
                    epsg_data = {"init" : "EPSG:" + str(item["properties"]["proj:epsg"])}
                    bbox = tuple(item["bbox"])

                    date_sensing = item["properties"]["datetime"].split("T")[0]
                    date_sensing = datetime.datetime.strptime(date_sensing, "%Y-%m-%d")
                    date_sensing = date_sensing.timestamp() # Converting the datetime string into seconds since epoch
                    
                    # Storing it as per the unique Sentinel 2 ID. If TCI is asked, TCI is added to the dictionary separately.
                    if self.TCI:
                        img_list.append({"img_id" : item['id'],"band_data" : band_data, "init" : "EPSG:" + str(item["properties"]["proj:epsg"]), "bbox" : bbox, "sensing_date" : date_sensing, "TCI" : item["assets"]["visual"]["href"]})
                    else:
                        img_list.append({"img_id" : item['id'],"band_data" : band_data, "init" : "EPSG:" + str(item["properties"]["proj:epsg"]), "bbox" : bbox, "sensing_date" : date_sensing})
                    pass

                pass
            pass

        # Checking if images are found
        if not img_list:
            return {start_date : [6, "[ERROR] No images could be found", tile_number]}
            pass

        choice = 0 # Variable for choosing the most recent image
        chosen_date = start_date
        # Choosing the most recent image
        for c, img_data in enumerate(img_list):
            sensing_date = img_data["sensing_date"]
            if sensing_date > min_datetime:
                min_datetime = sensing_date
                chosen_date = datetime.datetime.strftime(min_datetime, "%Y-%m-%d")
                choice = c

        return {chosen_date : [1, "[INFO] Found an image", img_list[choice]]}
        pass
    pass