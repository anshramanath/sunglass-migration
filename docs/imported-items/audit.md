# Imported Items Audit
_Last updated: 2026-05-30_

**Source:** `recategorized/categorized_items.json` → Supabase DB
**Brand:** BikerShades (`slug=bikershades`)

---

## Result

**Zero critical issues.** All row counts match expectations. No duplicate SKUs, no products missing images or categories.

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

| Depth | Categories |
|------:|-----------:|
| 1 | 8 |
| 2 | 18 |
| 3 | 28 |

8 root categories, max depth 3, matching the recategorize output.

---

## Data Quality

| Check | Result |
|-------|--------|
| Products with no images | 0 ✅ |
| Products with no categories | 0 ✅ |
| Duplicate product SKUs | 0 ✅ |
| Duplicate variation SKUs | 0 ✅ |
| Variations with no image | 108 ℹ️ (frontend falls back to product) |

---

## Notes

- 108 variations have no image — a mix of the 86 variations whose images were permanent 404s, plus others that never had variation-specific images in WooCommerce. Frontend falls back to parent product images.
- `product_images` (2,618) exceeds downloaded images (2,531) because some images are shared across products — the same Supabase URL can appear in multiple `product_images` rows.
