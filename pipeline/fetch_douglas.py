"""Douglas County Health Department's "Restaurant Inspection Records" -> data/raw/official/douglas/inspections.json (git-ignored).

Nick said yes on 2026-11-07 to scripting this public ArcGIS layer (item 2748cd3a55fb404da826a9f42f9eeb80; no license is stated on it).
Each record is one inspection: its date, the establishment's permit, name and address, and DCHD's own letter rating, with a link to the
county's PDF report. Shown as the county publishes it, dated and labeled as the county's; never a grade of ours. The layer's `Score`,
`Status` and `Match_*` fields are the geocoder's, not inspection results, so they aren't read.
Rules: one request at a time with a pause, robots.txt checked (pipeline/check_sources.py), a generic client name.
"""
import datetime, json, os, time
import requests

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(os.path.join(OUT, "douglas"), exist_ok=True)
ITEM = "https://www.arcgis.com/home/item.html?id=2748cd3a55fb404da826a9f42f9eeb80"
LAYER = "https://services.arcgis.com/pDAi2YK0L0QxVJHj/arcgis/rest/services/Restaurant_Inspections/FeatureServer/14"
FIELDS = ["inspection_id", "inspection_date", "permit_number", "firm_number", "est_name", "est_address", "est_city", "est_zip", "rating",
          "facility_types_primary", "facility_types_secondary", "downloadDetailsUrl"]
S = requests.Session(); S.headers["User-Agent"] = "EatsRankedData/1.0"
PAUSE = 2.0

n = S.get(LAYER + "/query", params={"where": "1=1", "returnCountOnly": "true", "f": "json"}, timeout=60).json()["count"]
rows, offset = [], 0
while offset < n:
    time.sleep(PAUSE)
    r = S.get(LAYER + "/query", params={"where": "1=1", "outFields": ",".join(FIELDS), "orderByFields": "ObjectID", "outSR": "4326",
                                        "resultOffset": offset, "resultRecordCount": 2000, "f": "json"}, timeout=120)
    r.raise_for_status()
    feats = r.json().get("features", [])
    if not feats:
        break
    for f in feats:
        a = dict(f["attributes"]); g = f.get("geometry") or {}
        a["lon"], a["lat"] = g.get("x"), g.get("y")
        rows.append(a)
    offset += len(feats)
    print(f"  {offset}/{n}")
assert len(rows) == n, (len(rows), n)
json.dump(rows, open(os.path.join(OUT, "douglas", "inspections.json"), "w"))
meta_p = os.path.join(OUT, "meta.json")
meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
meta["douglas"] = {"name": "Douglas County Health Department: Restaurant Inspection Records", "url": LAYER, "item": ITEM,
                   "fetched": datetime.date.today().isoformat(),
                   "through": max(a["inspection_date"] for a in rows if a.get("inspection_date")),
                   "terms": "a public ArcGIS layer of the Douglas County Health Department; no license stated; used with Nick's yes (2026-11-07)"}
json.dump(meta, open(meta_p, "w"), indent=1)
print("douglas inspections:", len(rows), "| through", meta["douglas"]["through"])
