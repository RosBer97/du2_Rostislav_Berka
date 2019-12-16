from quadtree import quadtree
import json

# load GeoJson file:
with open("input.geojson", "r", encoding = "utf-8") as f:
    data = json.load(f)
feat = data["features"]
feat_pok = feat[:200]

# features counter:
A = 0
cluster_id = 0
# calling recurse function
qtree_result = quadtree(feat_pok, A, 0)

gj_structure = {"type":"FeatureCollection"}
gj_structure["features"] = qtree_result


# save geojson file
with open("output.geojson", "w", encoding = "utf-8") as f:
    json.dump(gj_structure, indent = 2)

