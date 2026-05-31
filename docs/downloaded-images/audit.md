# Downloaded Images Audit
_Last updated: 2026-05-31_

**Source:** `migration/images/url_map.json` + `migration/images/failed.json`
**Items:** 581 | **Unique URLs:** 2,561 | **Downloaded:** 2,531 | **Failed:** 30

---

## Result

**All checks passed.** 2,531 images downloaded with zero missing files, zero zero-byte files, zero invalid extensions, and zero collisions. 30 permanent 404s tracked in `failed.json`.

---

## Counts

| Metric | Value |
|--------|------:|
| Items | 581 |
| URLs in `url_map` | 2,531 |
| Files on disk | 2,531 |
| In map but missing from disk | 0 |
| Zero-byte files | 0 |
| Invalid extensions | 0 |
| Failed downloads | 30 |
| Collisions | 0 |
| Items with no images | 0 |

---

## Coverage by Type

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| `product` | 1,450 | 0 | 1,450 |
| `variation` | 1,315 | 24 | 1,339 |
| `description` | 33 | 6 | 39 |
| `var_description` | 1 | 0 | 1 |
| **Total** | **2,531** | **30** | **2,561** |

---

## Failed Downloads

All 30 failures are permanent 404s — images that no longer exist on bikershades.com. All are variation or description images; no product loses all its images. Full list in `migration/images/failed.json`.

Notable patterns:
- Head-size graphic gallery images (gallery URL with `?i=` params) — 3 failures
- 2018 variation angle images for one product — 24 failures (all variation images for that product's color variants)
- 2018–2020 miscellaneous variation/description images — 3 failures

---

## Notes

- Image naming: path after `/uploads/` or `/gallery/` with `/` → `_` (e.g. `2024_05_image.jpg`). Globally unique — no collisions.
- `url_map.json` is the source of truth: `bikershades URL → local path`.
- Failed URLs are tracked in `failed.json` as `{failed_to_download: [{sku, src}], collisions: []}`.
- Collisions: 0 — naming scheme eliminates them by design.
