from quadtree import quadtree, acquire_bounding_points
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
feat = data["features"]
feat_pok = feat[:200] # just for testing of the algorithm

# features counter:
c_list = [0]
# acquire bounding points of rectangle/square set up by given points:
b_points = acquire_bounding_points(feat_pok)
# calling recurse function
qtree_result = []
quadtree(feat_pok, c_list, 0, qtree_result, b_points[0], b_points[1], b_points[2], b_points[3])
# odhalen problém s mizejícími body při skončení quadtree, z cca16 500 jich zbyde 16 000.
print("vstup",len(feat_pok))
print("vystup",len(qtree_result))

# build GeoJson:
gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = qtree_result

# build GeoJson–vstup:
gj_structure2 = {"type":"FeatureCollection"}
gj_structure2["features"] = feat_pok

# save output geojson file:
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure,f, indent = 2)
# save input geojson file:
with open("input_pouzity.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure2,f, indent = 2)

