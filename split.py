from quadtree import quadtree, acquire_bounding_points
import json

# load GeoJson file:
with open("input_Pan_Kyncl_Zastavky.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
# loading features to list feat
feat = data["features"]
feat_pokus = feat[:] # just for testing purposes, for reducing amount of data through slice index,
# for more comfortable work and visualisation in QGIS during developing

# features counter:
c_list = [0]
# acquire bounding points of rectangle/square set up by given points:
b_points = acquire_bounding_points(feat_pokus)
# calling recurse function
qtree_result = [] # final list with cluster_id
#input is list of given features, features counter, axis (0 or 1), list of outputfeatures, and bounding points)
quadtree(feat_pokus, c_list, qtree_result, b_points[0], b_points[1], b_points[2], b_points[3])

# build GeoJson:
gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = qtree_result

# save output geojson file:
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure,f, indent = 2)