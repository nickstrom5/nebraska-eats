# Nebraska Eats: name, icon and palette

**Final: Nick's decision of 2026-11-07 ("Yes, as proposed" on the 17-state review page).**
Name and icon C as below; the palette is the prompt's prairie-sky option, replacing the Husker-inspired scarlet.

## Name
- **Nebraska Eats**:
  - App Store name "Nebraska Eats: Restaurants" (26 characters).
  - Subtitle "Steaks, Reubens & Taquerías" (27).
  - Home Screen name "Nebraska Eats".
- Why, per the prompt: it has the best search fit, no App Store app has the name, and nebraskaeats.com is parked for sale.
- Alternatives:
  - "Nebraska Plates": the .com is unregistered, but it reads as license plates, and an app "Road Trip: Nebraska Plates" exists.
  - "Prairie Plates": no app has it, but the .com is taken.
- Avoided:
  - "Nebraska…The Good Life" (the welcome-sign slogan; "Good Life Eats®" is a blog's mark).
  - "Honestly, it's not for everyone" (a tourism line).
  - Husker, Cornhusker, Big Red and GBR (university marks).
  - "Omaha Dines" (an app) and Runza (a chain's trademark).

## Icon (state-prompts/ICON-STYLE.md; all three pass state-prompts/icon-style/check.swift)
- A: a T-bone steak, top view. At 60 px the bone reads as the letter T in a box. A two-lobed steak, tried too, reads as two circles.
- B: a bierock cut open (bun, crumb, beef-and-cabbage filling). At 60 px it's a generic stuffed bun.
- **C, chosen (final): a Reuben in side elevation** (rye, corned beef, Swiss, sauerkraut, rye). It reads as a sandwich at 60
  px, and it's Omaha's story (shown as a claim).
- Skipped, per the prompt: corn (the Iowa build's idea, and it leans Husker).
- `scripts/icon-concepts.swift` draws all three. `scripts/make-brand.swift` makes the app icon, favicons, touch icons and og.png from
  C.

## Palette (from the land; text contrast measured)
| Role | Hex | Contrast |
|---|---|---|
| Titles, tint, honors and oldest cards, icon background | prairie-sky blue #1D4E7A | 8.7:1 on white, 7.7:1 on cream; white on it 8.7:1 |
| Hand-checked guide cards, ink | charcoal #1F1F1F | white on it 16.5:1 |
| Pins, the title shadow, the header's ground (fill only) | Sandhills-grass gold #C9A24B | #1F1F1F on it 6.9:1; the sky-blue pin glyph on it 3.6:1; never text on white (2.4:1) |
| Small labels | sky blue #245A8A | 7.2:1 on white |
| Pages | cream #F5F1E7 | |
The first build's scarlet #D00000 is gone (2026-11-07).

## Header
One element: a prairie horizon with Chimney Rock's spire. It appears as Theme.swift's Stripes, make-site.py's RAYS and the band on
og.png.
