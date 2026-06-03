# fetch-products notes — Sunglass Monster

## Run

277 products fetched across 3 pages (100 / 100 / 77). No errors.

## Differences from ProSport

| | ProSport | Monster |
|---|---|---|
| Total products | 171 | 277 |
| Variable | 154 | 250 |
| Simple | 27 | 27 |
| No-SKU products | 1 (simple) | 5 (3 simple, 2 variable) |
| No-image products | 0 | 2 |
| Unique categories | 11 | 64 |
| Attribute names | 9 | 19 |
| Dimensions populated | 0/171 | 248/277 |
| short_description | 35/171 | 147/277 |
| "Uncategorized" tag | Every product | Not present |
| Flag status | draft | private |

## Things to handle downstream

- **Dimensions** — populated on Monster; keep at slim (ProSport dropped these)
- **No-SKU variable products** — 2 variable products have no SKU; will be flagged at validate and their variations never fetched
- **`"No category"`** — literal category name on 4 products; treat at categorize
- **`Choose Color (REQUIRED)`** — cleans to `Color` via `clean_attr_name` ✓
- **`Choose Bandana Color`** → `Bandana Color` (two words) — will trigger multi-word warn at reshape; acceptable for accessory products
- **`Cleaner Spray Bottle QTY`** → multi-word after clean — same, accessory product
