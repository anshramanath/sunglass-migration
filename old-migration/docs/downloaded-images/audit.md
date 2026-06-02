# Downloaded Images Audit
_Last updated: 2026-05-31_

**Source:** `migration/images/url_map.json` + `migration/images/failed.json`
**Items:** 573 | **Unique URLs:** 2,476 | **Downloaded:** 2,465 | **Failed:** 11

---

## Result

**All checks passed.** 2,465 images downloaded with zero missing files, zero zero-byte files, zero invalid extensions, and zero collisions. 11 permanent 404s tracked in `failed.json`.

---

## Counts

| Metric | Value |
|--------|------:|
| Items | 573 |
| URLs in `url_map` | 2,465 |
| Files on disk | 2,465 |
| In map but missing from disk | 0 |
| Zero-byte files | 0 |
| Invalid extensions | 0 |
| Failed downloads | 11 |
| Collisions | 0 |
| Items with no images | 0 |

---

## Coverage by Type

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| `product` | 1,421 | 0 | 1,421 |
| `variation` | 1,025 | 5 | 1,030 |
| `description` | 35 | 6 | 41 |
| **Total** | **2,465** | **11** | **2,476** |

---

## Failed Downloads

All 10 failures are permanent 404s — images that no longer exist on bikershades.com. No product loses all its images. Full list in `migration/images/failed.json`.

---

## Notes

- Down from 2,531 in run 2 — reflects variation images stripped when they duplicate a parent product image, variation description images removed entirely (now product-only), and the absorbed multiple-variation-images product adding 3 unique variation images.
- Image naming: path after `/uploads/` or `/gallery/` with `/` → `_`. Globally unique — no collisions.
- `url_map.json` is the source of truth: `bikershades URL → local path`.
