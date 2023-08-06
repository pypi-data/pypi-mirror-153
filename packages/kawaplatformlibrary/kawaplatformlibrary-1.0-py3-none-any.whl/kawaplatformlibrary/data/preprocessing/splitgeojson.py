import numpy as np
import json, argparse, datetime

from shapely.geometry import Point, Polygon, box, mapping, shape, LineString
from sklearn.metrics import pairwise_distances_argmin_min

from pathlib import Path

def degreeToKm(degree):
    return degree*111

def kmToDegree(distance_km):
    return distance_km/111


def getSatelliteCentroids(satellite_system):
    """
    Obtaining the geojson containing the satellite data polygon centroids

    Input Parameters :
        1. satellite_system => The satellite systems data is being obtained from

    Output Parameters : 
        1. List of coordinates of the centroids of the satellite data polygons
    """

    current_file_path = Path(__file__).parent.absolute()

    satellite_dict = {"SENTINEL2" : current_file_path/"satellitecentroids/sentinel2_centroid_geojsons.geojson"}

    with open(satellite_dict[satellite_system], "r") as in_file:
        geojson_contents = json.load(in_file)
        geojson_coordinates = geojson_contents["features"]
        in_file.close()
        pass

    return geojson_coordinates
    pass

def getClosestSatelliteCentroid(satellite_system, split_centroid_coords):
    """
    Obtaining the closest satellite polygon centroid to current point depending upon the satellite system

    Input Parameters :
        1. satellite_system      => Which satellite system is being used
        2. split_centroid_coords => The point to which the closest satellite polygon centroid has to be obtained

    Output Parameters :
        1. Returns the closest satellite polygon point
    """
    
    split_centroid_coords = list(*zip(*split_centroid_coords.coords.xy))

    satellite_centroid_geojson_features = getSatelliteCentroids(satellite_system)
    def get_centroid_coords():
        satellite_centroid_coordinates_list = []

        for coords in satellite_centroid_geojson_features:

            satellite_centroid_long = coords["geometry"]["coordinates"][0]
            satellite_centroid_lat  = coords["geometry"]["coordinates"][1]

            satellite_centroid_coordinates_list.append([satellite_centroid_long, satellite_centroid_lat])  
            pass

        return np.array(satellite_centroid_coordinates_list, dtype=np.float32)
        pass


    satellite_centroid_list = get_centroid_coords()
    split_geojson_coordinates = [[split_centroid_coords[0], split_centroid_coords[1]]]

    closest, _ = pairwise_distances_argmin_min(split_geojson_coordinates, satellite_centroid_list)

    return Point(satellite_centroid_list[closest][0])
    pass

def split(satellite_system, geojson_file, side_length_km=100):
    
    '''
    Splits a larger AOI into smaller AOIs of a desired side length.

    Input Parameters
    satellite_system => From which satellite system the data is being sourced
    geojson_file     => Coordinates of the AOI
    side_length_km   => side length of the square/tile desired

    Output Parameters
    '''


    user_poly = Polygon(geojson_file["coordinates"][0])
    usr_in = user_poly.buffer(kmToDegree(side_length_km/2),join_style=2)
    
    '''create a buffer around user input polygon and then create envelope
    start from one end of the box, find diagonally opposite point of side_lengthxside_length square
    draw the diagonal and find the centroid
    create buffer around centroid
    find next centroid within bounding box by moving side_length units along x axis'''
    
    env = usr_in.envelope # bounding box
    # print(env)
    start = Point(mapping(env)['coordinates'][0][0])  # startpoint

    p = Point(start.x + kmToDegree(side_length_km),start.y + kmToDegree(side_length_km)) # diagonally opposite point 
    cen_next_x = LineString([start, p]).centroid  # centroid along diagonal 

    final_geojsons = []

    half_side = side_length_km/2 # Size for calculating the buffer

    tenth_side = side_length_km/100


    # Finding the smaller polygons within the bounding box of the original AOI. 
    # First while loop is for the first row starting the from the bottom left corner
    # The second while loop is for the column starting with the current first row polygon. 
    while True:
        
        cen_satellite_next_x = getClosestSatelliteCentroid(satellite_system, cen_next_x) # Obtaining the closest satellite centroid

        buf_x = mapping(cen_satellite_next_x.buffer(kmToDegree(tenth_side),cap_style=3)) # buffer around centroid

        # Storing the polygon in final_geojsons, if the polygon intersects with the bounding box
        buf_shp_x = Polygon(buf_x["coordinates"][0])
        if usr_in.intersects(buf_shp_x):
            final_geojsons.append(buf_x)
            pass

        cen_next_y = cen_next_x # Making the initial y centroid the same as the x centroid 

        while True:
            cen_next_y = Point(cen_next_y.x + kmToDegree(0), cen_next_y.y + kmToDegree(side_length_km))

            cen_satellite_next_y = getClosestSatelliteCentroid(satellite_system, cen_next_y) # Obtaining the closest satellite centroid

            if not cen_next_y.within(env): # If the centroid calculated is beyond the bounding box, break the current loop
                break
                pass

            buf_y = mapping(cen_satellite_next_y.buffer(kmToDegree(tenth_side),cap_style=3))

            # Storing the polygon in final_geojsons, if the polygon intersects with the bounding box
            buf_shp_y = Polygon(buf_y["coordinates"][0])
            if usr_in.intersects(buf_shp_y):
                final_geojsons.append(buf_y)
                pass
            pass

        cen_next_x = Point(cen_next_x.x + kmToDegree(side_length_km),cen_next_x.y + kmToDegree(0))

        if not cen_next_x.within(env): # If the centroid calculated is beyond the bounding box, break the current loop
            break
            pass
        pass
            

    return final_geojsons
    # return centroids #for testing new split method 
    pass