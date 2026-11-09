"""Nebraska's open official records -> data/raw/official/ (git-ignored, never public).

Checked 2026-11-06 (playbook/12-sources.md):
- The Liquor Control Commission's "Active License Roster" (lcc.nebraska.gov/licensing-sdl/active-license-roster; an xlsx whose file name
  changes with each update): every active license with its class, number, trade name, address, city and county. Manager and licensee
  names are never read into the app. On-sale classes (A, C, I, AB, AD, IB, ID and the L/Y/Z taprooms) say a place pours on the premises;
  B and D are off-sale.
- Douglas County's "Restaurant Inspection Records" (ArcGIS item 2748cd3a55fb404da826a9f42f9eeb80) carries DCHD's official A-F rating, but
  the item states no license or terms, so it isn't read until Nick decides. NDA's inspection viewer and Lincoln-Lancaster's and Hall's
  searches are search-only (linked, never scraped).
One request at a time, honest user agent.
"""
import datetime, json, os, re, time, urllib.parse
import requests

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "official")
os.makedirs(os.path.join(OUT, "lcc"), exist_ok=True)
UA = "NebraskaEatsDataCheck/1.0 (+https://nickstrom5.github.io/nebraska-eats/; nick@eatsranked.com)"
S = requests.Session(); S.headers["User-Agent"] = UA
PAGE = "https://lcc.nebraska.gov/licensing-sdl/active-license-roster"
html = S.get(PAGE, timeout=60).text
links = re.findall(r'href="([^"]*Active[^"]*License[^"]*Roster[^"]*\.xlsx)"', html, flags=re.I)
assert links, "no roster link on the page"
url = urllib.parse.urljoin(PAGE, links[0])
time.sleep(1)
r = S.get(url, timeout=120); r.raise_for_status()
open(os.path.join(OUT, "lcc", "roster.xlsx"), "wb").write(r.content)
meta = {"lcc": {"name": "Nebraska Liquor Control Commission: Active License Roster", "page": PAGE, "url": url,
                "fetched": datetime.date.today().isoformat(), "terms": "a public roster published for download by the Commission; no license stated"}}
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("LCC roster:", url, len(r.content), "bytes")
