"""Official records for Nebraska -> one table of licensed businesses (playbook/12-sources.md).

The Liquor Control Commission's Active License Roster (statewide, bulk) is the one official list read: each active retail license with its
class, trade name and address. On-sale classes (C, I, A, AB, IB and the L brewery, Y farm-winery and Z microdistillery taprooms) say a
place pours on the premises; B and D are off-sale. Manager and licensee names are never read into the app (they are often people).
Inspections: NDA (most of the state) and the Douglas, Lancaster and Hall county health departments inspect restaurants. Douglas County
publishes DCHD's official A-F rating on a public ArcGIS layer, but the layer states no license or terms, so it isn't read until Nick
decides; the others are search-only. So no inspection result is shown and none is computed.

load() returns: jur, lic (our id), name, keys (name keys), addr, city, zip, num, street, lat, lon, kind, active, ltype, insp, biz.
"""
import os, re, json, datetime
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd
from common import norm_name, RAW, name_sim, _stems, GENERIC, canon_city

OFF = os.path.join(RAW, "official")
DIRS = {"N": "N", "S": "S", "E": "E", "W": "W", "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W"}
TYPES = set("ST STREET AVE AV AVENUE BLVD BOULEVARD RD ROAD DR DRIVE LN LANE CT COURT PL PLACE PKWY PARKWAY TER TRL TRAIL WAY HWY CIR "
            "CIRCLE PLZ SQ MALL BND PASS XING RUN ROW WALK RDG LOOP FWY FREEWAY EXPY EXPRESSWAY PIKE PK PKE".split())


def road(a):
    """One spelling for numbered roads. Nebraska writes one road as 'Route 100', 'US 7', 'Rt 2', 'NE 100' or 'NE Route 100', so every
    numbered US or state route is 'SH n' (as in ri-eats); 'N INTERSTATE 95' = 'I-95'; 'COUNTY ROAD 5' = 'CR 5'."""
    a = re.sub(r"(\d)\s*&\s*(\d)", r"\1-\2", a.upper())
    a = re.sub(r"\b(US|NE|SR|SH|CR|I|IH|RT|RTE)-(\w)", r"\1 \2", a)
    a = re.sub(r"\b(?:INTERSTATE(?: HIGHWAY| HWY)?|IH|I H)\s*(?=\d)", "I ", a)
    a = re.sub(r"\b(?:US|U S)\s+(?:HIGHWAY|HWY)\b", "US", a)
    a = re.sub(r"\b(?:FARM[- ]TO[- ]MARKET(?: ROAD| RD)?|FARM (?:ROAD|RD)|F M)\b", "FM", a)
    a = re.sub(r"\b(?:RANCH[- ]TO[- ]MARKET(?: ROAD| RD)?|RANCH (?:ROAD|RD)|RR|RM)\b(?=\s*\d)", "RM", a)
    a = re.sub(r"\b(?:STATE (?:HIGHWAY|HWY|ROAD|RD|ROUTE|RTE)|SR|SH|VERMONT (?:ROUTE|RTE|HIGHWAY|HWY)|NE (?:ROUTE|RTE|RT|HIGHWAY|HWY)|NE|"
               r"US (?:ROUTE|RTE|RT)|US|ROUTE|RTE|RT|HWY)\b\.?(?=\s*\d)", "SH", a)
    a = re.sub(r"\b(?:COUNTY (?:HIGHWAY|HWY|ROAD|RD)|CO RD|CTY (?:HWY|RD)|CR)\b", "CR", a)
    a = re.sub(r"\bHIGHWAY\b", "HWY", a)
    return re.sub(r"\b(US|SH|CR|HWY|FM|RM|I) (\w+)\s*-\s*\w+", r"\1 \2", a)


ORD = {"FIRST": "1ST", "SECOND": "2ND", "THIRD": "3RD", "FOURTH": "4TH", "FIFTH": "5TH", "SIXTH": "6TH", "SEVENTH": "7TH",
       "EIGHTH": "8TH", "NINTH": "9TH", "TENTH": "10TH", "ELEVENTH": "11TH", "TWELFTH": "12TH"}


def street_key(a):
    """'2505 Monroe St' -> ('2505', 'MONROE'); '1000 OSAGE STREET' -> ('1000', 'OSAGE'); 'E Colfax Ave' keeps 'COLFAX'."""
    if not isinstance(a, str):
        return None, None
    a = re.sub(r"[.,#]", " ", road(a))
    # "20940-A North Frederick Ave": a hyphenated unit letter is part of the number (Maryland's Montgomery County wrote them so)
    m = re.match(r"^\s*(\d+)(?:-?[A-Z])?(?:\s*-\s*\d+[A-Z]?)?\s+(.*)$", a)
    if not m:
        return None, None
    words = [w for w in m.group(2).split() if w]
    if len(words) > 1 and words[0] in DIRS:
        words = words[1:]
    core = []
    for w in words:
        if w in TYPES and core:
            break
        core.append(w)
    core = [ORD.get(w, w) for w in core]
    return m.group(1), " ".join(core[:3]) or None


def street_compat(a, b):
    """Same street, or one is a whole-word prefix of the other: Boulder's 2025 set sometimes truncates ("1206 CENTAUR" = Centaur Village Dr)."""
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
        return False
    return a == b or a.startswith(b + " ") or b.startswith(a + " ")


def street_nums(a):
    """'157-159 W Main St' -> {'157', '159'}; '2505 Monroe St' -> {'2505'}."""
    if not isinstance(a, str):
        return set()
    a = road(a)
    m = re.match(r"^\s*(\d+)[A-Z]?(?:\s*-\s*(\d+)[A-Z]?)?\s", a.upper() + " ")
    if not m:
        return set()
    lo = int(m.group(1)); hi = int(m.group(2)) if m.group(2) else lo
    if hi < lo:   # "1500-02"
        hi = int(str(lo)[: len(str(lo)) - len(m.group(2))] + m.group(2)) if m.group(2) else lo
    return {str(x) for x in range(lo, hi + 1, 2 if (hi - lo) % 2 == 0 else 1)} if 0 <= hi - lo <= 12 else {str(lo)}


def _names(*vals):
    out = []
    for v in vals:
        if not isinstance(v, str):
            continue
        v = re.sub(r"\s*\((?:MOBILE|MOBILE UNIT|COMMISSARY|CATERING|SPECIAL EVENT|SPEC EVENT|TEMP(?:ORARY)? EVENT|CP|INSIDE [^)]*)\)\s*$", "", v, flags=re.I)
        for part in re.split(r"\s*/\s*|\s+\bdba\b\s+|\s+&\s+(?=[A-Z][a-z])", v, flags=re.I):
            k = norm_name(re.sub(r"\b(?:LLC|INC|CORP|CORPORATION|LTD|CO)\b\.?", "", part, flags=re.I))
            if k and k not in out:
                out.append(k)
    return out


META = json.load(open(os.path.join(OFF, "meta.json"))) if os.path.exists(os.path.join(OFF, "meta.json")) else {}
LIST_DATE = (META.get("lcc") or {}).get("fetched")   # the day we read the roster (the file name carries its month and day)
THROUGH = None
MPLS_PAGE = "https://lcc.nebraska.gov/licensing-sdl/active-license-roster"
# NDA's food inspection report viewer (OnBase; search-only, so it is only linked); Douglas, Lancaster and Hall run their own searches
INSPECTIONS_URL = "https://nda.nebraska.gov/fscp/foods/inspection_areas.html"
ONPREM_T = ("Nebraska on-sale liquor license (beer, wine and spirits)", "Nebraska on-sale beer license")
MAKER_T = ("Nebraska craft brewery license", "Nebraska farm winery license", "Nebraska microdistillery license")
RESULTS = ()


def liq_kind(t):
    """A license type as shown -> on-premises or retail."""
    if not isinstance(t, str):
        return None
    return "onprem" if t in ONPREM_T or t in MAKER_T else "retail" if "off-sale" in t else None


def lcc_class(c):
    """An LCC class -> (kind, license type as shown, drinks)."""
    c = (c or "").strip().upper()
    if c in ("C", "I", "IB", "ID", "CK"):
        return "food", ONPREM_T[0], ["beer", "wine", "liquor"]
    if c in ("A", "AB", "AD", "AK"):
        return "food", ONPREM_T[1], ["beer"]
    if c == "L":
        return "food", MAKER_T[0], ["beer"]
    if c == "Y":
        return "food", MAKER_T[1], ["wine"]
    if c == "Z":
        return "food", MAKER_T[2], ["liquor"]
    if c in ("B", "D"):
        return "retail", "Nebraska off-sale liquor license", None
    return "other", f"Nebraska liquor license (class {c or '?'})", None


COLUMNS = ["jur", "lic", "name", "dba", "holder", "keys", "addr", "city", "zip", "num", "street", "lat", "lon", "kind", "active", "ltype",
           "insp", "issued", "biz", "drinks", "county"]


def _zip(z):
    z = re.sub(r"\D", "", str(z or ""))
    return z[:5] if len(z) >= 5 else ""


def _addr(a):
    """'2790 VETERANS MEMORIAL BLVD STE 130' -> '2790 Veterans Memorial Blvd Ste 130'."""
    a = re.sub(r"\s+", " ", a or "").strip()
    return re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).title(), a)


def _city(c):
    return canon_city(" ".join(w.capitalize() for w in str(c or "").split())) if isinstance(c, str) and c.strip() else None


def _ms(v):
    """An ArcGIS date (epoch milliseconds, UTC) -> YYYY-MM-DD in Nebraska's time (the district's own day)."""
    if not isinstance(v, (int, float)):
        return None
    d = datetime.datetime.fromtimestamp(v / 1000, datetime.timezone.utc) - datetime.timedelta(hours=4)
    return d.date().isoformat()


def load_lcc():
    x = pd.read_excel(os.path.join(OFF, "lcc", "roster.xlsx"), dtype=str)
    rows = []
    for r in x.to_dict("records"):
        if (r.get("License Type Group") or "") != "Retail" or (r.get("License State") or "") != "Active":
            continue
        kind, lt, drinks = lcc_class(r.get("Class"))
        name = re.sub(r"\s+", " ", str(r.get("Trade Name") or "")).strip()
        lines = [l.strip() for l in re.split(r"_x000D_|\n", str(r.get("Address") or "")) if l.strip()]
        addr = _addr(lines[0]) if lines else ""
        z = re.search(r"\b(\d{5})(?:-\d{4})?\b", lines[-1]) if len(lines) > 1 else None
        num, st = street_key(addr)
        cty = str(r.get("County") or "").strip()
        rows.append({"jur": "lcc", "lic": "lcc-" + str(r.get("License Number") or "").strip(), "name": name, "dba": name, "holder": None,
                     "keys": _names(name), "addr": addr, "city": _city(r.get("City")), "zip": z.group(1) if z else "", "num": num, "street": st,
                     "lat": None, "lon": None, "kind": kind, "active": True, "ltype": lt, "insp": [], "issued": None, "drinks": drinks,
                     "county": None, "apn": None})
    return rows


def load():
    """The LCC's active retail licenses, one row each (no inspections are read; see the docstring)."""
    rows = load_lcc() if os.path.exists(os.path.join(OFF, "lcc", "roster.xlsx")) else []
    df = pd.DataFrame(rows) if rows else pd.DataFrame({c: pd.Series(dtype=object) for c in COLUMNS + ["apn"]})
    for c_ in COLUMNS:
        if c_ not in df.columns:
            df[c_] = None
    df["lat"] = df["lat"].astype(float); df["lon"] = df["lon"].astype(float); df["active"] = df["active"].astype(bool)
    df["biz"] = np.arange(len(df))
    return df
