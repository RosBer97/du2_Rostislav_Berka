from quadtree import quadtree
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
feat = data["features"]
feat_pok = feat[:] # just for testing of the algorithm

# features counter:
c_list = [0]
# calling recurse function
qtree_result = []
quadtree(feat_pok, c_list, 0, qtree_result)

print("vstup",len(feat_pok))
print("vystup",len(qtree_result))

# build GeoJson:
gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = qtree_result

# save geojson file:
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure,f, indent = 2)

