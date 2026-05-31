# Downloaded Images Verify
_Last updated: 2026-05-31_

**Source:** All image URLs across 581 items cross-referenced against `url_map.json` and `failed.json`

---

## Result

**All checks passed.** All 2,561 image URLs are accounted for — either downloaded (2,531) or permanently failed (30). No URL is unaccounted for. No product is left imageless.

---

## Checks

| Check | Result |
|-------|--------|
| All 2,561 URLs accounted for (in map or failed) | ✅ |
| No URL in both url_map and failed.json | ✅ |
| No extra URLs in url_map absent from items | ✅ |
| No product has all product images failed | ✅ |

---

## Counts

| Metric | Value |
|--------|------:|
| URLs in items | 2,561 |
| In `url_map` | 2,531 |
| In `failed.json` | 30 |
| Unaccounted | 0 |
| Products with no images | 0 |
| Variations with no images | 86 |

---

## Notes

- 86 variations have no images — expected; frontend falls back to parent product images.
- No product lost all its product images to 404s — every product has at least one downloadable image.
- `2,531 + 30 = 2,561` — accounts for 100% of URLs.
