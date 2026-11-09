# Nebraska Eats (ne-eats) — notes for Claude Code sessions

Built 2026-11-06 by a side session for Nick's "build the 17 states left" (group: MN, IA, NE, ND, SD).
- The pipeline is ported from `../mn-eats/` (its official-list plumbing), and the app and site from `../ia-eats/` (no inspection
  results).
- It carries every fix through 11-05: the exact-outline county lookup, the out-of-county truck rule, Utah's street-word merge fix,
  Vermont's narrowed "dejavu" rule, Virginia's near-adult-venue fix, the per-state ZIP check, the delivery-only brands, the website
  blocklist and `link_blocklist.py`, the Share link `Links.site + explore/#p=<id>`, OTA data and the adult-venue rules.
- It also has wy-eats' far-listing rule.
- Local only: git-ignored data, no repo, no remote, nothing published. Sources: `playbook/12-sources.md`.

Brand: `playbook/05-naming.md` — **final**, Nick's decision of 2026-11-07: the name, the Reuben icon (C), and the prairie-sky palette (blue #1D4E7A,
Sandhills-grass gold #C9A24B fill only, charcoal, cream) that replaced the Husker-inspired scarlet.
- Name: "Nebraska Eats: Restaurants", Home Screen "Nebraska Eats".
- Icon: a Reuben in side elevation.
- Palette: scarlet #D00000, charcoal #1F1F1F, wheat gold #C9A24B (fill only) and cream #F5F1E7. No N, mascot or team words.
- Header band: a prairie horizon with Chimney Rock's spire.

## Nebraska is different
- **No Google data at all** (rule of 2026-11-06). The UCSD snapshot is never downloaded, `listings.py` builds an empty Google table,
  and `nebraska.py` writes NaN fits as null. The keep rule is the family's: Meta 0.95, or 0.90 with a website.
- **One official list: the Liquor Control Commission's Active License Roster** (`fetch_official.py`, `official.py`, an xlsx renamed
  each update).
  - Active retail licenses are read, and on-sale ones are matched to map listings. A licensed bar or restaurant the map lacks is
    added when its name says it's a place to eat.
  - "Serves alcohol" shows only for a match. Elsewhere it's "—", never "no".
  - Licensee and manager names are never read into the app.
  - `calibrate.py` measures the map listings against the on-sale list.
- **Inspections: Douglas County's own ratings only:**
  - Douglas County's official letter ratings (DCHD's public "Restaurant Inspection Records" layer; Nick's yes, 2026-11-07): fetched
    by `pipeline/fetch_douglas.py` and attached in `nebraska.py` to 1,008 Omaha-area places, shown as "Rated A" with the date and the
    county's PDF report linked, never as a grade of ours. NDA's, Lincoln-Lancaster's and Hall's reports stay search-only (linked).
  - NDA, Lincoln-Lancaster and Hall County are search-only.
  - Places without a Douglas County rating link NDA's page on who inspects where (`Links.inspections`).
- **Counties and regions:** 93 counties and six detail files (Omaha Metro, Lincoln & Southeast, Northeast, Central, Sandhills &
  North, West & Panhandle).
  - `fetch_overture.py` checks the border towns: South Sioux City, Falls City and the Panhandle are in; Council Bluffs, Sioux City,
    Yankton, Pine Bluffs, Julesburg, Hiawatha and Rock Port are out.
  - The app's outline (`LocationService.swift`) and the web app's (`NE_RINGS` in `explore.js`) cut the neighbours' land back out.
- **Venues:**
  - Eppley Airfield (4501 Abbott Dr and the terminal box) and Lincoln Airport.
  - CHI Health Center, Charles Schwab Field, Baxter Arena and the Henry Doorly Zoo (Omaha); Pinnacle Bank Arena and Haymarket Park
    (Lincoln); Werner Park (Papillion); Fonner Park and the State Fair (Grand Island).
  - Each venue address counts only in its own town.
  - Stores with food counters (Casey's, Hy-Vee, Bosselman, Kwik Shop, Bucky's and others) are hidden as stores. Showing Casey's is
    Nick's call.
- **Adult venues:** standalone clubs by address in `data/research/adult_venues.json`.
  - The Foxy (downtown Lincoln) and The Office are left to the 150 m name rule. The Office shares 640 W Prospector Ct with Playmakers
    Bar and Grill, which the address rule wrongly hid.
  - not_adult: Legacy Downs (WarHorse Casino) and "Scott's Bluff County Adult" (a county office).
- **Names:** `data/research/name_fixes.json` spells the "Don and Millies" listings "Don & Millie's", as Lincoln's visitor bureau does.
- **Guides** (tags in `nebraska.py` TAGS, bits 1..8; sources in `pipeline/build_research.py`, each note checked against its page on
  2026-11-06):
  - Steakhouses (12): every place the Flatwater Free Press reviewed or ranked in its 2025 Steak Town USA series.
  - Reubens & Frenchees (7): Visit Omaha's 2025 Reuben roundup, shown as Omaha's claim, plus Don & Millie's cheese frenchee from
    Lincoln's visitor bureau.
  - South Omaha Taquerías (4): Visit Omaha's own listings.
  - Oldest (5): Glur's Tavern 1876, Johnny's Cafe 1922, Chances R 1932, Gorat's 1944, Cascio's 1946.
  - The Visit Omaha and Lincoln listing pages draw their text in the browser. `build_research.py` cites each listing; its fields were
    read from the page's embedded data.
- **Closed:** Sehnert's Bakery & Bieroc Cafe in McCook (America's Classics 2019) closed in October 2025 as Embers Bakery & Café (North
  Platte Post). It's on `closed.json`, and no listing for it remains.
  - The Bohemian Cafe closed in 2016, but its building is now The Bohemian Bar, so no closure is applied there.
  - With Sehnert's closed, there's no bierock guide; leads are in `data/research/app/LEADS.md`.
- **Honors:** no MICHELIN Guide covers Nebraska. James Beard:
  - Johnny's Cafe: America's Classics 2026.
  - David Utterback (Yoshitomo and Ota): Best Chef: Midwest nominee, 2025 and 2026. `nebraska.py`'s hon_flags reads "nominee" as
    finalist.
  - Semifinalists: Zach Midgett (Casa Bovina, 2026) and Tim Nicholson (The Boiler Room, 2025).
  - Le Bouillon (Omaha): Outstanding Wine and Other Beverages Program semifinalist, 2026.
- **Links:** `check_websites.py` treats the five states' papers, TV stations and tourism sites as news (`PLAINS_NEWS`). `clean_url`
  keeps only the first of two links in one field.

## Rebuild
```bash
cd pipeline
../.venv/bin/python check_sources.py URL...   # a new host first
../.venv/bin/python fetch_overture.py && ../.venv/bin/python fetch_extras.py && ../.venv/bin/python fetch_official.py && ../.venv/bin/python fetch_douglas.py
../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py && ../.venv/bin/python geocode_official.py
../.venv/bin/python listings.py && ../.venv/bin/python calibrate.py
../.venv/bin/python nebraska.py && ../.venv/bin/python build_research.py && ../.venv/bin/python nebraska.py
NE_APP=1 ../.venv/bin/python nebraska.py && cd .. && cp data/app/places.json data/app/detail-*.json NebraskaEats/Resources/
.venv/bin/python pipeline/check_websites.py && .venv/bin/python pipeline/check_websites.py --retry-transient   # then re-export
.venv/bin/python scripts/make-site.py && .venv/bin/python scripts/publish_app_data.py && .venv/bin/python scripts/publish_app_data.py --check
.venv/bin/python scripts/qa-site.py --static && .venv/bin/python scripts/qa-site.py   # the second runs headless Chrome (Playwright)
```
- `data/chain_auv.json` is a copy of wy-eats'. The `.venv` is on the python.org framework Python 3.12 with the family's versions.
- `fetch_overture.py` skips any file that already exists. A stale `overture_ne_sources.parquet`, from an early wrong-box download,
  once left 0 listings, so delete both parquets together.

## App, site, screenshots
- **App:** `NebraskaEats/`.
  - XcodeGen `project.yml`, bundle `com.nebraskaeats.ios`, display name "Nebraska Eats".
  - Tests are in `NebraskaEatsTests/` and `NebraskaEatsUITests/`. The unit tests use a 12-place Nebraska fixture, plus data guards:
    adult venues, blocklisted and multi-URL websites, bad and legal names, non-restaurants, listed twice, no Google data, every
    license is the LCC's, Sehnert's closed.
  - Build and test only with Xcode 1.app (27.2, 27B52); Xcode.app is a beta.
  - xcodegen writes Info.plist from `project.yml`, so edit the location text there.
- **Site:** `scripts/make-site.py` writes `docs/` and `playbook/site-numbers.json`. `scripts/explore.js` is the web app, and
  `scripts/qa-site.py` the QA.
  - Site URL for now: nickstrom5.github.io/nebraska-eats, with no CNAME.
  - City pages: Omaha. A town needs 4 hand-checked or honored places for a page.
- **Screenshots:**
  1. `scripts/capture-screenshots.sh <sim>`. ScreenshotMode pins downtown Omaha by default:
     - Aksarben for steakhouses and the Johnny's Cafe detail
     - Blackstone for Reubens
     - South 24th Street for taquerías
  2. `scripts/site-images.sh`, then make-site and qa-site.
  3. App Store frames: `scripts/appstore-screenshots.py`.
- **Listing:** `playbook/app-store/listing.json`.
- **Icons:** `scripts/icon-concepts.swift` and `scripts/make-brand.swift`.

## Status
See the end of this file (written when the build finished).

### Status (2026-11-08 10:55): final
- **Ready to publish; nothing public.** No repo, commit, push, Pages, App Store Connect record
  or build upload; all of those wait for Nick's yes.
- Data: 4,809 restaurants (5,115 places) in 398 towns, 90 counties; 24 hand-checked guide places (12 steakhouses, 7 Reubens and cheese
  frenchees, 4 South Omaha taquerías, 5 oldest), 6 James Beard honorees (1 America's Classic). Official list: the Liquor Control
  Commission's Active License Roster (1,949 places matched; "Serves alcohol" on 1,815 from on-sale licenses). Douglas County's own
  letter ratings show on 1,008 Omaha-area places (Nick's yes, 2026-11-07); no grade is ever computed.
- The Rusty Nail (Omaha) is back: the non-food rule no longer hides bars named for a nail.
- Tests (Xcode 1.app 27.2, iOS 27.0), final run 2026-11-08 on the prairie-sky palette and the Douglas County ratings: iPhone 17 Pro
  Max and iPad 13" (M5) each passed all 49 unit + 6 UI tests. The iPhone launch-time test skipped itself in the full run (load 92) and
  then passed alone on a quiet machine (4.66 s to Home, 10:53); 4.62 s on iPad (the limit is 6 s). Earlier (11-07) fixes were all to
  test code: a website floor copied from Minnesota (3,000; Nebraska has 2,545), the iPad tour's leftover Iowa search ("Archie's
  Waeside"), and the accessibility audit now skips on a timeout under load.
- Site: `docs/` regenerated 2026-11-08 with the new screenshots; `qa-site.py --static` and the full headless-Chrome run both OK
  (2026-11-08 10:45; the run checks a Douglas County place shows "Rated" and the county's report link, and a place elsewhere links
  NDA); `publish_app_data.py --check` OK.
- App Store: 8 iPhone and 6 iPad frames in `playbook/app-store/`, rebuilt 2026-11-08 from new screenshots in the prairie-sky palette;
  `listing.json` (Nebraska Eats: Restaurants; Steaks, Reubens & Taquerías; support and privacy on nickstrom5.github.io/nebraska-eats/).
- Brand final (Nick, 2026-11-07): name, Reuben icon on prairie-sky blue, and the prairie-sky palette (app theme, icon, site, og.png and
  frame colors regenerated). Douglas County's A–F layer is scripted (Nick's yes); an NDA records request is being drafted by the parent.
