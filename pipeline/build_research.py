"""Writes data/research/app/*.json (hand-checked Nebraska guides), data/research/michelin.json, jbf.json and closed.json from the compact
lists below. Ported from ia-eats/pipeline/build_research.py.

Each entry cites the pages that name it, read on 2026-11-06: the Flatwater Free Press's 2025 "Steak Town USA" series (its critic's
ranking of December 18, 2025, its reviews and its 2022 history of Omaha steakhouses), Visit Omaha's own Reuben guide (February 12, 2025)
and listings, Lincoln's visitor bureau listings, Tasting Table's dated lists, the North Platte Post, The Reader and jamesbeard.org.
omaha.com, journalstar.com, KETV, WOWT, Omaha Magazine and 1011 Now disallow Claude in robots.txt and visitnebraska.com answers with a bot
check, so none is cited. Readers' polls aren't used.
The address comes from the map listing we already hold for that name in that town (site/nebraska.json); a name that isn't found exactly
once in its town (or at the street number given) is left out and listed in data/research/app/LEADS.md. A place the map data doesn't show
as a place to eat is added only with the street address its listing gives (ADDR).
Usage: ../.venv/bin/python build_research.py   (then nebraska.py)"""
import json, os, re, unicodedata
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "nebraska.json")))
C, M = d["cols"], d["meta"]
# accents folded ("Taquería" is "Taqueria"), apostrophes dropped
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", unicodedata.normalize("NFKD", (s or "").lower().replace("'", "").replace("’", ""))
                                             .encode("ascii", "ignore").decode())).strip()

FFP = "https://flatwaterfreepress.org/"
FFP_RANK = FFP + "steak-town-usa-its-time-to-pick-the-best-omaha-steakhouse/"                          # 2025-12-18
FFP_HIST = FFP + "a-brief-history-of-omaha-steakhouses-past-and-present/"                               # 2022-02-18
FFP_YORK = FFP + "steak-town-usa-in-york-steak-comes-with-a-side-of-history-and-community/"             # 2025-07-23
FFP_SPEAK = FFP + "steak-town-usa-down-a-remote-road-find-a-ghost-town-and-one-of-nebraskas-best-steaks/"   # 2025-04-17
VO = "https://www.visitomaha.com/"
VO_REUBEN = VO + "blog/post/think-outside-the-bun-with-omahas-reuben-offerings/"                         # 2025-02-12
VO_L = VO + "listings/"
LNK_DM1 = "https://www.lincoln.org/listing/don-&-millies/559/"                                            # Lincoln CVB listing
LNK_DM2 = "https://www.lincoln.org/listing/don-&-millies/431/"                                            # Lincoln CVB listing
TT_OLDREST = "https://www.tastingtable.com/1975409/oldest-restaurant-every-state-still-open/"   # 2025-09-23
TT_OLDBAR = "https://www.tastingtable.com/1786324/oldest-bar-every-state/"                      # 2025-02-17
JBF = "https://www.jamesbeard.org/stories/"
JBF_AC26 = JBF + "james-beard-americas-classics-award-winners-2026"                              # 2026-02-25
JBF_NOM26 = JBF + "james-beard-awards-restaurant-and-chef-nominees-2026"                         # 2026-03-31
JBF_NOM25 = JBF + "2025-james-beard-awards-restaurant-and-chef-nominees"                         # 2025-04-02
JBF26 = JBF + "james-beard-award-semifinalists-2026"                                             # 2026-01-21
JBF25 = JBF + "the-2025-james-beard-award-semifinalists"                                         # 2025-01-22
NPP_EMBERS = "https://northplattepost.com/posts/b47a7fff-766f-4f5c-88fd-5dbe573f60e7"           # 2025-10-20
READER_BOHO = "https://thereader.com/2016/08/11/the-long-goodbye-of-the-bohemian-cafe-concludes-sept-24/"   # 2016-08-11
OMA, LNK = "Omaha", "Lincoln"
CRITIC = "the Flatwater Free Press's critic"

GUIDES = {
 "nebraska steakhouse": [   # the Flatwater Free Press's Steak Town USA series (2025): every place it reviewed and ranked
  ("Committee Chophouse", OMA, None, f"Ranked Omaha's best steakhouse by {CRITIC} (December 2025), in the renovated Cottonwood Hotel in "
   "Blackstone.", None, None, [FFP_RANK]),
  ("The Drover", OMA, "2121", f"The \"most beloved Omaha steakhouse\" of {CRITIC} (December 2025); it opened in 1968 as Cork and Cleaver "
   "and became The Drover in 1979.", None, None, [FFP_RANK, FFP_HIST]),
  ("801 Chophouse", OMA, None, "The downtown chophouse dry-ages its beef for at least 28 days (Flatwater Free Press, December 2025).",
   None, None, [FFP_RANK]),
  ("Pivot Prime", OMA, None, "A new steakhouse near 132nd and West Dodge, known for its beef tallow candle (Flatwater Free Press, "
   "December 2025).", None, None, [FFP_RANK]),
  ("Ruhlman's Steakhouse", "Ashland", None, "Ashland's steakhouse, known for its wood-fired toffee skillet cookie (Flatwater Free Press, "
   "December 2025).", None, None, [FFP_RANK]),
  ("Jerico's", OMA, "11732", "Prime rib and a banana cream pie made in-house daily (Flatwater Free Press, December 2025); open since 1978.",
   None, None, [FFP_RANK, FFP_HIST]),
  ("Johnny's Cafe", OMA, "4702", f"The Stockyards steakhouse Frank Kawa opened in 1922, still run by his family; {CRITIC} calls its onion "
   "rings Omaha's best (December 2025).", 1922, "Flatwater Free Press (2022): opened in 1922, at 4702 S. 27th St.", [FFP_RANK, FFP_HIST, JBF_AC26]),
  ("Brother Sebastian's", OMA, "1350", "Open since 1977 and reopened eight months after a 1996 fire; the St. Thomas filet is its steak "
   "(Flatwater Free Press, December 2025).", None, None, [FFP_RANK, FFP_HIST]),
  ("Gorat's", OMA, "4917", "Open since 1944 on Center Street; its meat sauce follows a 1940s Gorat family recipe (Flatwater Free Press, "
   "December 2025).", 1944, "Flatwater Free Press (2022): opened in 1944, at 4917 Center St.", [FFP_RANK, FFP_HIST]),
  ("Cascio's", OMA, None, "Old-school Italian recipes and a housemade spaghetti sauce, at its location since the 1940s (Flatwater Free "
   "Press).", 1946, "Flatwater Free Press (2022): opened in 1946, \"at its current location in the 1940s\".", [FFP_RANK, FFP_HIST]),
  ("Chances R", "York", "124", "York's \"pillar known statewide and built on beef and hospitality,\" a classic Interstate 80 stop "
   "(Flatwater Free Press, July 2025).", 1932, "Flatwater Free Press (July 2025): it started in 1932 as the Cozy Lunch, a burger shop, in "
   "what is now its east-side dining room.", [FFP_YORK]),
  ("The Speakeasy", "Holdrege", "72993", "A small-town steakhouse in the ghost town of Sacramento, a few miles from Holdrege: \"The big draw "
   "... is really the beef\" (Flatwater Free Press, April 2025).", None, None, [FFP_SPEAK])],
 "omaha reuben": [   # Visit Omaha's own Reuben guide (2025-02-12); Lincoln's visitor bureau for the cheese frenchee
  ("Crescent Moon", OMA, None, "Visit Omaha says it \"proudly serves the original\" Blackstone Reuben, and Reuben egg rolls. Omaha claims "
   "the Reuben was first made at the Blackstone Hotel; New York claims it too.", None, None, [VO_REUBEN]),
  ("Barchen Beer Garden", OMA, None, "One of Visit Omaha's picks for a Reuben (February 2025).", None, None, [VO_REUBEN]),
  ("Barrett's Barleycorn Pub & Grill", OMA, None, "One of Visit Omaha's picks for a Reuben (February 2025).", None, None, [VO_REUBEN]),
  ("Brazen Head Irish Pub", OMA, None, "One of Visit Omaha's picks for a Reuben, with Reuben nachos too (February 2025).", None, None,
   [VO_REUBEN]),
  ("Dundee Dell", OMA, None, "One of Visit Omaha's picks for a Reuben (February 2025).", None, None, [VO_REUBEN]),
  ("Wilson & Washburn", OMA, None, "One of Visit Omaha's picks for a Reuben (February 2025).", None, None, [VO_REUBEN]),
  ("Don & Millie's", LNK, "8150", "Lincoln's visitor bureau lists its made-from-scratch cheese frenchee, the breaded, fried cheese "
   "sandwich.", None, None, [LNK_DM1]),
  ("Don & Millie's", LNK, "5200", "Lincoln's visitor bureau lists its made-from-scratch cheese frenchee, the breaded, fried cheese "
   "sandwich.", None, None, [LNK_DM2])],
 "south omaha taqueria": [   # Visit Omaha's own listings
  ("Taqueria El Rey", OMA, "5201", "On South 24th Street; to Visit Omaha \"the tacos are a must,\" with tortas, gorditas, sopes and steak "
   "fries.", None, None, [VO_L + "taqueria-el-rey-24th-st/69031/"]),
  ("El Ranchito", OMA, "4318", "On South 24th Street: homemade food served fast, with complimentary chips and street tacos (Visit Omaha).",
   None, None, [VO_L + "el-ranchito/66034/"]),
  ("Dos De Oros", OMA, "3310", "\"The Taco Truck\" on South 24th Street, a local favorite for traditional Mexican tacos (Visit Omaha).",
   None, None, [VO_L + "dos-de-oros/63631/"]),
  ("Taqueria El Alteño", OMA, "4871", "Tacos and traditional Mexican soups on L Street (Visit Omaha).", None, None,
   [VO_L + "el-alte%C3%B1o-taqueria/69054/"]),
  ("Tixteco", OMA, "2203", "A family-run South Omaha restaurant: tacos, tortas, burritos, tostadas and fresh soups, and a house margarita "
   "guests swear by (Visit Omaha).", None, None, [VO_L + "tixteco/68051/"])],
 "oldest": [
  ("Glur's Tavern", "Columbus", "2301", "Tasting Table names it Nebraska's oldest restaurant and its oldest bar, serving Columbus since 1876.",
   1876, "Tasting Table (2025): open since 1876.", [TT_OLDREST, TT_OLDBAR])],
}
ADDR = {("Jerico's", OMA): "11732 W Dodge Rd"}   # Flatwater Free Press (2022); the map data has no listing for it
CUISINE = {("Glur's Tavern", "Columbus"): "Bar & Pub"}
KINDS = {k: [k] for k in ("nebraska steakhouse", "omaha reuben", "south omaha taqueria", "oldest")}

# MICHELIN: no guide covers Nebraska (guide.michelin.com/us/en/nebraska/restaurants answered 404 in September 2026)
MICHELIN = []
MI_MATCH = {}
MI_UT = None
MID = "Best Chef: Midwest"
JBF = [{"name": "Johnny's Cafe", "city": OMA, "honors": ["America's Classics 2026"], "sources": [JBF_AC26]},
       {"name": "Yoshitomo", "city": OMA, "honors": [f"{MID} nominee 2026 and 2025 (David Utterback)"], "sources": [JBF_NOM26, JBF_NOM25]},
       {"name": "Ota", "city": OMA, "honors": [f"{MID} nominee 2026 and 2025 (David Utterback)"], "sources": [JBF_NOM26, JBF_NOM25]},
       {"name": "Casa Bovina", "city": LNK, "honors": [f"{MID} semifinalist 2026 (Zach Midgett)"], "sources": [JBF26]},
       {"name": "The Boiler Room", "city": OMA, "honors": [f"{MID} semifinalist 2025 (Tim Nicholson)"], "sources": [JBF25]},
       {"name": "Le Bouillon", "city": OMA, "honors": ["Outstanding Wine and Other Beverages Program semifinalist 2026"], "sources": [JBF26]}]
CLOSED = [{"name": "Embers Bakery & Café", "address": None, "city": "McCook",
           "match_names": ["EMBERS BAKERY", "EMBERS BAKERY & CAFE", "EMBERS BAKERY AND CAFE", "SEHNERTS BAKERY", "SEHNERTS BAKERY & BIEROC CAFE",
                           "SEHNERTS BAKERY AND BIEROC CAFE", "SEHNERTS"],
           "closed_reason": "Closed in October 2025, ending nearly seven decades downtown: it opened as Sehnert's Bakery in 1957, won a James "
                            "Beard America's Classics award in 2019, and became Embers Bakery & Café after its 2021 sale.",
           "sources": [NPP_EMBERS]}]


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"\s+", " ", re.sub(r"\band\b", " ", re.sub(r"^the ", "", norm(s)))).strip()   # "Don & Millie's" is "Don and Millies"


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = name
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

MI_ADDR = {}
json.dump({"restaurants": [{"name": n, "address": MI_ADDR.get(n), "city": t, "zip": None, "distinction": dist, "cuisine": cu, "green_star": False,
                             "michelin_url": MI_UT, "sources": [MI_UT], "match_names": [x.upper() for x in MI_MATCH.get(n, [])], "open": True}
                            for n, t, dist, cu in MICHELIN]}, open(f"{R}/michelin.json", "w"), indent=1, ensure_ascii=False)
json.dump([dict({"address": None}, **j, zip=None, open=True) for j in JBF], open(f"{R}/jbf.json", "w"), indent=1, ensure_ascii=False)
json.dump(CLOSED, open(f"{R}/closed.json", "w"), indent=1, ensure_ascii=False)
open(f"{R}/app/LEADS.md", "w").write("# Nebraska research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a source we may use, or for the map data
- Bierocks: Sehnert's Bakery & Bieroc Cafe (McCook; America's Classics 2019) closed in October 2025 as Embers Bakery & Café (closed
  list). Runza is a chain and its trademark (facts only), so no bierock guide yet.
- Czech kolaches and dinners: Clarkson Bakery's kolaches (Nebraska Life, 2023) and Wilber's Sokol Hall bakers (Flatwater Free Press,
  October 2026, not a restaurant) have no 2025-26 page naming a place to eat; the Czech and Slovak museum's café (Omaha) is inside a
  museum. Omaha's Bohemian Cafe closed in 2016 (The Reader); its building, 1406 S 13th St, is now The Bohemian Bar, which the map
  data shows, so no closure is applied there.
- Cheese frenchees: Amigos/Kings Classic (Tasting Table, 2022) has no 2025-26 page; Don & Millie's carries it on Lincoln's visitor
  bureau listings.
- Steakhouses statewide: the Flatwater Free Press's "every steakhouse in Nebraska" list gives names and addresses only, so its places
  wait for a page that describes them.
- Official data: Douglas County's official letter ratings (bulk, no license stated) wait for Nick; NDA, Lincoln-Lancaster and Hall
  County inspections are search-only; the LCC's Active License Roster is used.
- Blocked or unusable hosts: omaha.com, journalstar.com, ketv.com, wowt.com, omahamagazine.com, 1011now.com, omahadailyrecord.com,
  knopnews2.com, ksnblocal4.com and mccookgazette.com disallow Claude; visitnebraska.com answers with a bot check.
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)
