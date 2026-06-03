# import-items audit — proSPORT Sunglasses

## Row counts

| Table | DB | Expected |
|---|---|---|
| `products` | 166 | 166 ✓ |
| `variations` | 1713 | 1713 ✓ |
| `categories` | 12 | — |
| `product_categories` | 197 | — |
| `product_images` | 565 | — |
| `variation_images` | 36 | — |
| `description_images` | 143 | — |

## Brand

- `proSPORT Sunglasses` (slug=`prosport`)

## Category tree depth

| Depth | Categories |
|---|---|
| 1 (roots) | 4 |
| 2 (leaves) | 8 |

4 root categories: Shop By Style, Lens Color, Readers Special Fit, Accessories (root-level leaf). 8 leaf categories across them.

## Data quality

| Check | Count |
|---|---|
| Products with no images | 0 |
| Products with no categories | 0 |
| Variations with no image | 1677 |
| Duplicate product SKUs | 0 |
| Duplicate variation SKUs | 0 |
| `product_images` sort_order range | 1–13 |

1677/1713 variations have no variation-specific image — they fall back to the parent product's image gallery on the frontend. The 36 variations with images have a unique image not present in the parent's gallery.
