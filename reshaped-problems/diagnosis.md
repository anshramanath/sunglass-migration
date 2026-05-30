# Reshaped Problems Overview

This folder tracks manual review work for products flagged during reshaping.

## Files

- [zero_price_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/zero_price_review.md:1)
- [no_weight_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/no_weight_review.md:1)
- [no_image_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/no_image_review.md:1)
- [invalid_sku_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/invalid_sku_review.md:1)
- [missing_attributes_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/missing_attributes_review.md:1)
- [duplicate_name_review.md](/Users/anshramanath/Desktop/bikershades-migration/reshaped-problems/duplicate_name_review.md:1)

## High-Level Status

| Bucket | Review File | Status | High-Level Direction |
| --- | --- | --- | --- |
| Zero price | `zero_price_review.md` | Reviewed | Mostly owner review; a few are excludes, one needs price, several are form/workflow decisions |
| No weight | `no_weight_review.md` | Reviewed | Mostly owner review; some real products need confirmed weight now |
| No image | `no_image_review.md` | Reviewed | Mostly owner review; try to recover real images before using placeholders |
| Invalid SKU | `invalid_sku_review.md` | Reviewed | Mostly owner review; many items are real products that need canonical SKU cleanup |
| Missing attributes | `missing_attributes_review.md` | Built | Take entire bucket to owner; variation metadata is not recoverable confidently |
| Duplicate name | `duplicate_name_review.md` | Built | Take entire bucket to owner; duplicated names need rename/merge/split decisions |

## Bucket Notes

### Zero price

- Main themes: hidden/internal pages, dynamic Rx forms, real products with missing price, and unavailable items.
- Main outcome: almost everything should be run by the owner before final migration decisions.

### No weight

- Main themes: shipping/service items, accessories, combo products, and Rx/configurable products.
- Main outcome: some items just need a confirmed weight, while others need owner confirmation on whether the workflow/product still belongs on the new site.

### No image

- Main themes: broken or missing parent images, replacement parts, and at least one product that looks like stale/broken media.
- Main outcome: ask owner for real images where possible; only use placeholders with explicit approval.

### Invalid SKU

- Main themes: service items, RX option/add-on pages, products whose SKU is really a label or product name, and products with dirty SKUs that may just need cleanup.
- Main outcome: most entries need owner confirmation of the canonical SKU and whether the item should still exist as a standalone product/workflow.

### Missing attributes

- Main themes: products where some variations are missing usable option metadata in both reshaped `attribute` and nested variation `variation` fields.
- Main outcome: take the whole bucket to the owner because the missing data is not safe to reconstruct blindly.

### Duplicate name

- Main themes: distinct products collapsing to the same reshaped name.
- Main outcome: take the whole bucket to the owner to decide whether the products should be renamed, merged, split, or excluded.

## Current Priority Read

1. Owner review is the main blocker for `duplicate_name`, `missing_attributes`, and most of `invalid_sku`.
2. `no_weight` and `zero_price` contain the most direct “fix and migrate” opportunities once the owner answers a few questions.
3. `no_image` is probably the easiest media cleanup bucket if the owner still has the missing assets.
