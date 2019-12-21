from turtle import exitonclick
from quadtree_drawing import draw_points
from quadtree import quadtree, acquire_bounding_points
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
# loading features to list feat
feat = data["features"]
feat_reduced = feat[:] # just for testing purposes, for reducing amount of data through slice index,
# for more comfortable work and visualisation in QGIS during developing, it will be deleted in
# final version

if len(feat_reduced) < 2:
    print("Too small list of points, list should have at least 2 points – features")

else:

    # It was quite difficult to invent how to add original cluster ID to all clusters. This list called counter_list
    # is for this purpose. It has only one element – zero. It is sent to the quadtree function. In this function
    # + 1 is added in every step of end condition (less than 50 elements in the list). So, at the end of function quadtree
    # its not zero, it is bigger number and it says how many clusters are in given data.
    counter_list = [0]
    # acquire bounding points of rectangle/square set up by given points:
    b_points = acquire_bounding_points(feat_reduced)

    ################ TURTLE DRAWING #################  turtle draw all points in list feat_reduced
    config_tuple = draw_points(feat_reduced, b_points[0], b_points[1], b_points[2], b_points[3])

    # calling recurse function
    #input is list of given features, features counter, list of output features, and bounding points)
    quadtree(feat_reduced, counter_list, b_points[0], b_points[1], b_points[2], b_points[3], config_tuple)

    # stop turtle drawing
    exitonclick()

    # build GeoJson:
    gj_structure = {"type":"FeatureCollection"}
    gj_structure["features"] = feat_reduced

    # save output geojson file:
    with open("output.geojson", "w", encoding = "utf-8") as f:
        json.dump(gj_structure,f, indent = 2)