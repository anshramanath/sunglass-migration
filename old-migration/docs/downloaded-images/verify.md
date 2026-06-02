# Downloaded Images Verify
_Last updated: 2026-05-31_

**Source:** All image URLs across 573 items cross-referenced against `url_map.json` and `failed.json`

---

## Result

**All checks passed.** All 2,476 image URLs are accounted for — either downloaded (2,465) or permanently failed (11). No product is left imageless.

---

## Checks

| Check | Result |
|-------|--------|
| All 2,476 URLs accounted for (in map or failed) | ✅ |
| No URL in both url_map and failed.json | ✅ |
| No extra URLs in url_map absent from items | ✅ |
| No product has all product images failed | ✅ |

---

## Counts

| Metric | Value |
|--------|------:|
| URLs in items | 2,476 |
| In `url_map` | 2,465 |
| In `failed.json` | 11 |
| Unaccounted | 0 |
| Products with no images | 0 |
| Variations with no images | 10 |

---

## Notes

- 10 variations have no images — frontend falls back to parent product images.
- `2,465 + 11 = 2,476` — 100% of URLs accounted for.
