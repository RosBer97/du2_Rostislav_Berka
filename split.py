from quadtree import quadtree
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
feat = data["features"]
feat_pok = feat[:200]

# features counter:
c_list = []
# original ID for every group:
cluster_id = 0
# calling recurse function
qtree_result = []
final = quadtree(feat_pok, c_list, 0, qtree_result)


gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = final


# save geojson file
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dumps(gj_structure, indent = 2)

