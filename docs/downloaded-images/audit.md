# Downloaded Images Audit
_Last updated: 2026-05-31_

**Source:** `migration/images/url_map.json` + `migration/images/failed.json`
**Items:** 574 | **Unique URLs:** 2,477 | **Downloaded:** 2,467 | **Failed:** 10

---

## Result

**All checks passed.** 2,467 images downloaded with zero missing files, zero zero-byte files, zero invalid extensions, and zero collisions. 10 permanent 404s tracked in `failed.json`.

---

## Counts

| Metric | Value |
|--------|------:|
| Items | 574 |
| URLs in `url_map` | 2,467 |
| Files on disk | 2,467 |
| In map but missing from disk | 0 |
| Zero-byte files | 0 |
| Invalid extensions | 0 |
| Failed downloads | 10 |
| Collisions | 0 |
| Items with no images | 0 |

---

## Coverage by Type

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| `product` | 1,422 | 0 | 1,422 |
| `variation` | 1,026 | 4 | 1,030 |
| `description` | 35 | 6 | 41 |
| **Total** | **2,467** | **10** | **2,477** |

---

## Failed Downloads

All 10 failures are permanent 404s — images that no longer exist on bikershades.com. No product loses all its images. Full list in `migration/images/failed.json`.

---

## Notes

- Down from 2,531 in run 2 — reflects variation images stripped when they duplicate a parent product image, variation description images removed entirely (now product-only), and the absorbed multiple-variation-images product adding 3 unique variation images.
- Image naming: path after `/uploads/` or `/gallery/` with `/` → `_`. Globally unique — no collisions.
- `url_map.json` is the source of truth: `bikershades URL → local path`.
