# create-items notes — proSPORT Sunglasses

## Results

- Input: `reshape-products/products.json` (169 products) + `reshape-variations/variations.json` (1740 variations across 152 products)
- Passed: 166 → `create-items/items.json` (150 variable, 16 simple; 1713 variations embedded)
- Flagged: 3 → `create-items/flagged.json`

All 3 flagged products trace back to the 18 variations excluded at `validate_variations.py` — their variation IDs appear in the product's `variations[]` list but were never written to reshape-variations.

## What this step does

For each variable product, replaces the `variations[]` array of IDs with the actual variation objects from `reshape-variations`. Simple products pass through unchanged.

## Phases

**Phase 1 — Fill variations**
Iterate reshape-variations entries. For each entry, find the matching product by `product_id`. For each variation in the entry, swap it into the product's `variations[]` at the slot matching its `id` — only if:
- `variation.id` matches the ID slot being replaced
- `variation.parent_id` matches the product `id`

Unmatched IDs remain as integers in the array.

**Phase 2 — Per-item checks (run on all)**
- Unreplaced IDs → flag entire product
- Variable product with no filled variations → flag
- Attribute expansion: for each variation attribute, if the name exists in the parent's attributes, add the option if missing. If the name doesn't exist in the parent at all → flag.
- Attribute prune: remove options no variation uses; drop empty attributes
- Image dedup: remove any entry from a variation's `images[]` whose `src` matches a `src` in the parent's `images[]`; result is `[]` if all deduped
- Min/max price: `minPriceCents` = min variation `regularPriceCents`; `maxPriceCents` = max
- Sale: `True` if any variation has `sale=True`; cross-checked against WC `sale` value from reshape
- `variations[]` cleaned to only filled objects (unreplaced ints dropped)

**Phase 3 — Global SKU uniqueness**
Check-before-add across all product SKUs and variation SKUs. Duplicates flag the entire product.

## Design decisions

- **Ownership triple-check** — variation is only swapped in if its `id` matches the slot AND its `parent_id` matches the product. The grouped structure of reshape-variations provides a third implicit check (the variation came from the same `product_id` entry).
- **Flag entire product** — if any variation ID is unreplaced, the whole product is excluded. Partial items are not written to `items.json`.
- **Attribute expansion not flagging** — if a variation uses an option the parent didn't list, the option is added to the parent rather than flagging. This corrects WooCommerce data where parent attribute options weren't updated when new variations were added. The check is: name must match a parent attribute; if the name itself is absent, that is flagged.
- **Image dedup** — 1677 of 1713 variations (97.9%) have `images: []` after dedup. Only 36 variations carry a unique image not present in the parent's `images[]`.
- **Min/max from `regularPriceCents`** — uses the stable "was" price, not the current selling price, so the range doesn't change when sales start/stop.
- **`salePriceCents` stays null at product level** — sale pricing is per-variation only.
