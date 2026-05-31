# Downloaded Images Audit
_Last updated: 2026-05-30_

**Source:** `recategorized/categorized_items.json`
**Items:** 581 | **Unique URLs:** 2,561

---

## Result

**Zero critical issues.** All 2,531 downloaded files are present on disk. 30 failures are confirmed 404s — files permanently deleted from the server.

---

## Summary

| Metric | Count |
|--------|------:|
| Items | 581 |
| URLs in `url_map.json` | 2,531 |
| Files on disk | 2,531 |
| In map but missing from disk | 0 |
| Zero-byte files | 0 |
| Invalid extensions | 0 |
| Failed downloads | 30 |
| Collisions | 0 |
| Items with all product images failed | 0 |

---

## Coverage by Type

| Type | Downloaded | Failed | Total |
|------|----------:|-------:|------:|
| Product images | 1,450 | 0 | 1,450 |
| Variation images | 1,315 | 24 | 1,339 |
| Description images | 33 | 6 | 39 |
| Variation description images | 1 | 0 | 1 |

All product-level images downloaded successfully. 24 variation images and 6 description images are confirmed 404s.

---

## Failed Downloads

All 30 failures are HTTP 404 — the server confirmed these files no longer exist. Mostly 2018-era images deleted from WordPress. Not recoverable.

| SKU | URL |
|-----|-----|
| `CFM85X11MN-COMBOS` | `.../gallery/head-size-graphic/S_MD_headsize_3_1600.jpg?i=616353724` |
| `FM21X05CM-0-YL` | `.../uploads/2020/11/XS_SM_headsize_3_1600.jpg` |
| `FM540405CB-BK-CL-MFB-2` | `.../uploads/2018/01/2-Clear-Angle-6.jpg` |
| `GO00X47BBEE-BK-CL-MFB-1` | `.../uploads/2018/01/Angle-13.jpg` |
| `GO84X75BL-BK-CL-MFLG-2` | `.../uploads/2018/02/Angle-17.jpg` |
| `FM8X8BC-0-CL` | `.../uploads/2018/05/MED_XL_headsize_3_1600-1024x352.jpg` |
| `FM8X8BC-GY-YLIM-MFB-1` | `.../uploads/2018/05/Grey-Tinted-Yellow-Angle.jpg` |
| `FM85X11MNA-BK-MOR-MFB-3` | `.../uploads/2018/01/Black-Orange-Mirror-Angle.jpg` |
| `FM85X11MNA-BK-SM-MFB-3` | `.../uploads/2018/01/Black-Smoke-Angle.jpg` |
| `FM85X11MNA-BK-YL-MFB-3` | `.../uploads/2018/01/Black-Yellow-Angle.jpg` |

Full list in `migration/images/failed.json`.

---

## Notes

- Images are named using the path after `/uploads/` or `/gallery/` with `/` replaced by `_` — guaranteed unique, no collisions possible.
- The 30 failed URLs will not be inserted into the DB at import time. Frontend falls back to parent product images for variations with missing images.
