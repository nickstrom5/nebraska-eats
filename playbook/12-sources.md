# Nebraska sources and calibration (checked 2026-11-06)

## Official sources
| Source | What it has | Can a script read it? | Used |
|---|---|---|---|
| Liquor Control Commission "Active License Roster" (lcc.nebraska.gov/licensing-sdl/active-license-roster; an xlsx renamed each update) | class, license number, state, trade name, address, city, county | yes, a public download | yes: 6,961 active retail licenses read on 2026-11-06, 3,607 of them on-sale (classes A, C, I, AB, AD, IB, ID and the L/Y/Z taprooms); 2,101 matched to map listings, 320 licensed bars and restaurants added; 1,814 app places show "Serves alcohol". Licensee and manager names are never shown |
| Douglas County Health Department "Restaurant Inspection Records" (ArcGIS item 2748cd3a55fb404da826a9f42f9eeb80) | inspections with the county's official A–F rating | yes, a public layer | no: no license or terms stated, so it's Nick's call. If it's used, show the county's letter as published and dated, and compute nothing |
| NDA inspections (ecmp.nebraska.gov OnBase viewer) | items marked IN/OUT | search-only | no; a records request (§84-712) is Nick's call |
| Lincoln-Lancaster (ephportal.lincoln.ne.gov) and Hall County (Central District, inspectionsonline.us) | inspections | search-only (Lincoln's has reCAPTCHA) | no |
| NDA "who inspects where" (nda.nebraska.gov/fscp/foods/inspection_areas.html) | which agency inspects each county | page | linked from every place |
| NE OCIO Statewide Parcels | building values | yes | no: there's no property-value board, and its terms limit use to "within the state" (ask Nick first) |

## Coverage of the LCC's on-sale list (calibrate.py)
- How often each kind of map listing matched an on-sale license:
  - Meta 0.95+: 32.5%
  - Meta 0.90 with a website: 22.2%
  - BrightQuery 0.95+: 7.7%
- An on-sale license marks only the places that pour, so these shares are low by nature.
- 44.9% of the 3,607 on-sale licensees are among the open map listings.
- The keep rule is the family's: Meta 0.95, or 0.90 with a website.
- No Google data is read anywhere.

## Counts
- App: 5,115 places, 4,808 restaurants in 398 towns (Census CBP 2023: 4,371 NAICS 722 establishments).
- Web: 6,283 places.
- Overture: 9,148 eating and drinking listings in Nebraska, 438 of them marked closed.
- Casey's and Hy-Vee counters are hidden with the non-restaurants. Whether they appear is Nick's call.

## Research hosts (check_sources.py)
- **Usable:** flatwaterfreepress.org, visitomaha.com, lincoln.org, tastingtable.com, thereader.com, northplattepost.com,
  nebraskalife.com, nebraskapublicmedia.org, klkntv.com, unomaha.edu, visitkearney.org, visitgrandisland.com, grandisland.com,
  siouxcityjournal.com, nebraskatravelerguide.com, jamesbeard.org.
- **Blocked by robots.txt:** omaha.com, journalstar.com, ketv.com, wowt.com, omahamagazine.com, 1011now.com, omahadailyrecord.com,
  knopnews2.com, ksnblocal4.com, mccookgazette.com.
- **Other:** visitnebraska.com answers with a bot check, and travelnebraska.org didn't answer.
- Visit Omaha's and Lincoln's listing pages draw their text in the browser. Each listing's own fields (address, description) sit in
  the page's embedded data, read by script.
