from shapely.geometry import shape, Polygon, Point

def createBBox(pos, side_km):

    side_km = 0.009120 * side_km
    min_lat = pos[1] - side_km
    max_lat = pos[1] + side_km
    min_lon = pos[0] - side_km
    max_lon = pos[0] + side_km

    lower_left  = Point(min_lon, min_lat)
    lower_right = Point(max_lon, min_lat)
    upper_right = Point(max_lon, max_lat)
    upper_left  = Point(min_lon, max_lat)

    point_list = [lower_left, lower_right, upper_right, upper_left]

    poly = Polygon([[p.x, p.y] for p in point_list])

    polyg = poly.exterior.coords

    coords = []
    for x,y in polyg:
        coords.append([x,y])
        pass

    gj = {"type" : "Polygon", "coordinates" : [coords]}

    return gj
    pass