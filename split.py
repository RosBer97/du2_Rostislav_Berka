from quadtree import quadtree, acquire_bounding_points
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
feat = data["features"]
feat_pok = feat[:] # just for testing of the algorithm

# features counter:
c_list = [0]
# acquire bounding points of rectangle/square set up by given points:
b_poits = acquire_bounding_points(feat_pok)
# calling recurse function
qtree_result = []
quadtree(feat_pok, c_list, 0, qtree_result, b_poits[0], b_poits[1], b_poits[2], b_poits[3])
# odhalen problém s mizejícími body při skončení quadtree, z cca16 500 jich zbyde 16 000.
print("vstup",len(feat_pok))
print("vystup",len(qtree_result))

# build GeoJson:
gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = qtree_result

# save geojson file:
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure,f, indent = 2)

