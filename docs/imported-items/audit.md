# Imported Items Audit
_Last updated: 2026-05-31_

**Source:** Supabase DB
**Products:** 581 | **Variations:** 5,649 | **Categories:** 54

---

## Result

**All checks passed.** Row counts match source exactly. No products without images or categories. No duplicate SKUs.

---

## Row Counts

| Table | DB | Expected |
|-------|---:|--------:|
| `products` | 581 | 581 ✅ |
| `variations` | 5,649 | 5,649 ✅ |
| `categories` | 54 | — |
| `product_categories` | 1,082 | — |
| `product_images` | 2,618 | — |
| `description_images` | 935 | — |

---

## Category Tree

| Depth | Count |
|-------|------:|
| 1 | 8 |
| 2 | 18 |
| 3 | 28 |

---

## Data Quality

| Check | Result |
|-------|--------|
| Products with no images | 0 ✅ |
| Products with no categories | 0 ✅ |
| Variations with no image | 108 (frontend falls back to product) |
| Duplicate product SKUs | 0 ✅ |
| Duplicate variation SKUs | 0 ✅ |

---

## Brands

- BikerShades (`slug=bikershades`)
