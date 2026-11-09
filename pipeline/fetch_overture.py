"""Download the Overture Maps extracts that nebraska.py reads -> data/ne/

- overture_ne_bbox.parquet     every place in Nebraska's bounding box (name, category, address, point)
- overture_ne_sources.parquet  which datasets each Nebraska eating/drinking listing came from (Meta, Foursquare, ...)
- ne_shapes.json               simplified state and county outlines for the map
- ne_state_detail.geojson      the state outline at full detail, for the in-state test

Reads the public Overture bucket over S3 with DuckDB (no account needed). Ported from mn-eats/pipeline/fetch_overture.py.
Nebraska: land division areas; the "counties" are its 93. The script checks the towns on its river and straight lines (Omaha and
Council Bluffs, South Sioux City and Sioux City, Nebraska City, Falls City, Kimball and Pine Bluffs) so an Iowa, South Dakota, Missouri,
Kansas, Colorado or Wyoming listing stays out.
"""
import os, json, time
import duckdb
from shapely import wkb
from shapely.geometry import mapping, Polygon

RELEASE = "2026-10-21.0"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "ne")
# Nebraska (40.00°N–43.00°N, 95.31°W–104.05°W) plus a margin for the border towns (Omaha-Council Bluffs, South Sioux City, Kimball)
BBOX = "bbox.xmin BETWEEN -104.2 AND -95.2 AND bbox.ymin BETWEEN 39.9 AND 43.1"
EAT = "('restaurant','casual_eatery','bar','fast_food_restaurant','coffee_shop','cafe','smoothie_juice_bar','brewery','food_court')"
os.makedirs(OUT, exist_ok=True)

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
places = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=places/type=place/*.parquet"

t = time.time()
if not os.path.exists(f"{OUT}/overture_ne_bbox.parquet"):
    con.execute(f"""
COPY (
  SELECT id, names.primary AS name, basic_category AS cat, taxonomy.primary AS tax, taxonomy.hierarchy AS hier, confidence,
         operating_status AS status, brand.names.primary AS brand, addresses[1].freeform AS street, addresses[1].locality AS city,
         addresses[1].postcode AS zip, addresses[1].region AS region, ST_Y(geometry) AS lat, ST_X(geometry) AS lon, websites[1] AS web,
         phones[1] AS phone
  FROM read_parquet('{places}', hive_partitioning=1) WHERE {BBOX}
) TO '{OUT}/overture_ne_bbox.parquet' (FORMAT PARQUET)""")
    print("places in bbox", round(time.time() - t), "s", flush=True)
if not os.path.exists(f"{OUT}/overture_ne_sources.parquet"):
    con.execute(f"""
COPY (
  SELECT id, list_transform(sources, lambda x: x.dataset) AS ds, list_transform(sources, lambda x: x.update_time) AS ut,
         list_transform(sources, lambda x: x.record_id) AS rid,
         len(socials) AS n_soc, len(websites) AS n_web, len(phones) AS n_ph
  FROM read_parquet('{places}', hive_partitioning=1)
  WHERE {BBOX} AND basic_category IN {EAT}
) TO '{OUT}/overture_ne_sources.parquet' (FORMAT PARQUET)""")
    print("sources", round(time.time() - t), "s", flush=True)

areas = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=divisions/type=division_area/*.parquet"
rows = con.execute(f"""
  SELECT subtype, names.primary AS name, ST_AsWKB(geometry) AS g
  FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region = 'US-NE' AND subtype IN ('region', 'county') AND class = 'land'
    AND bbox.xmin > -104.3 AND bbox.xmax < -95.1 AND bbox.ymin > 39.8 AND bbox.ymax < 43.2""").fetchall()


def rings(geom, tol, min_area):
    geom = geom.simplify(tol, preserve_topology=True)
    polys = [p for p in getattr(geom, "geoms", [geom]) if p.geom_type == "Polygon" and p.area >= min_area]
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys]


out = {"state": None, "counties": []}
for sub, name, g in rows:
    geom = wkb.loads(bytes(g)).buffer(0)
    if sub == "region":
        json.dump(mapping(geom.simplify(0.0005, preserve_topology=True)), open(f"{OUT}/ne_state_detail.geojson", "w"))
        out["state"] = [[r] for r in rings(geom, 0.002, 0.000005)]
    else:
        out["counties"].append({"name": name, "c": rings(geom, 0.004, 0.00002)})
# full-detail county polygons for assigning each place to a county (not shipped)
json.dump({name: mapping(wkb.loads(bytes(g)).buffer(0).simplify(0.0003, preserve_topology=True))
           for sub, name, g in rows if sub == "county"}, open(f"{OUT}/ne_counties_detail.geojson", "w"))
json.dump(out, open(f"{OUT}/ne_shapes.json", "w"), separators=(",", ":"))
print("outlines: state", len(out["state"] or []), "rings +", len(out["counties"]), "counties;", round(time.time() - t), "s total")
# border towns: each must fall on the right side of the detailed state outline
from shapely.geometry import shape, Point
st = shape(json.load(open(f"{OUT}/ne_state_detail.geojson")))
for nm, lon, lat, want in [("Omaha", -95.9345, 41.2565, True), ("Bellevue", -95.8908, 41.1544, True), ("South Sioux City", -96.4136, 42.4739, True),
                           ("Nebraska City", -95.8597, 40.6775, True), ("Falls City", -95.6019, 40.0608, True), ("Kimball", -103.6630, 41.2361, True),
                           ("Scottsbluff", -103.6672, 41.8666, True), ("Chadron", -103.0010, 42.8294, True), ("Valentine", -100.5510, 42.8728, True),
                           ("Council Bluffs, IA", -95.8608, 41.2619, False), ("Sioux City, IA", -96.4003, 42.4999, False), ("North Sioux City, SD", -96.4831, 42.5272, False),
                           ("Yankton, SD", -97.3973, 42.8711, False), ("Hiawatha, KS", -95.5355, 39.8525, False), ("Pine Bluffs, WY", -104.0691, 41.1822, False),
                           ("Julesburg, CO", -102.2643, 40.9886, False), ("Hamburg, IA", -95.6577, 40.6064, False), ("Rock Port, MO", -95.5169, 40.4114, False),
                           ("Elk Point, SD", -96.6836, 42.6833, False)]:
    ok = st.contains(Point(lon, lat))
    print(f"  {nm}: {'inside' if ok else 'outside'}{'' if ok == want else '  <-- WRONG'}")
print("counties:", len(out["counties"]), sorted(c["name"] for c in out["counties"]))

# the neighbours' land (Iowa, Missouri, Kansas, Colorado, Wyoming, South Dakota): listings.py widens Nebraska's outline ~300 m for
# river banks, but only where no neighbour's land is, so a Council Bluffs or Sioux City listing on the far side of the river stays out
nb = con.execute(f"""
  SELECT region, ST_AsWKB(geometry) FROM read_parquet('{areas}', hive_partitioning=1)
  WHERE country = 'US' AND region IN ('US-IA', 'US-MO', 'US-KS', 'US-CO', 'US-WY', 'US-SD') AND subtype = 'region' AND class = 'land'""").fetchall()
from shapely.ops import unary_union
from shapely.geometry import box
near = box(-104.3, 39.8, -95.1, 43.2)
nbg = unary_union([wkb.loads(bytes(g)).buffer(0).intersection(near) for _, g in nb])
json.dump(mapping(nbg.simplify(0.0002, preserve_topology=True)), open(f"{OUT}/ne_neighbors.geojson", "w"))
print("neighbours:", sorted(r for r, _ in nb))
