# Single-Leaf Items Review
_Last updated: 2026-05-31_

**Source:** `recategorized/single_leaf_items.json`

These 3 products are the sole occupant of their leaf category — no other product shares that leaf. The recategorizer removes such leaves to avoid stub categories with only one product. Owner decides: add more products to the category, merge into a parent, or drop the product.

---

## Products

### PM 2.5 Medical Face Masks – PACK OF THREE!
- **SKU:** `clothmasks`
- **WpUrl:** https://bikershades.com/shop/accessories/safety-protection/cotton-face-mask/
- **Leaf category:** `accessories → safety-protection`
- **Situation:** Only product in `safety-protection`. An accessory but doesn't fit neatly into other accessory subcategories.
- **Action needed:** Owner decides — keep `safety-protection` leaf and populate it with more products, place under plain `accessories`, or drop this product from the new site.

---

### Chopper 901 Fits SM-LG
- **SKU:** `CH8CP901-0`
- **WpUrl:** https://bikershades.com/shop/motorcycle-sunglasses/lens-type/smoke-grey/chopper-901/
- **Leaf category:** `motorcycle-sunglasses → brands → chopper`
- **Situation:** Only product under the `chopper` brand leaf. Had many lens-type categories but all were stripped as non-leaf paths; only the brand leaf remained, and it's a singleton.
- **Action needed:** Owner decides — add more Chopper products, merge into `motorcycle-sunglasses → brands`, or recategorize under a lens-type leaf alongside other products.

---

### BikerArmour Pinkie [SM – MED]
- **SKU:** `FM63X32PK-0`
- **WpUrl:** https://bikershades.com/shop/motorcycle-sunglasses/shop-by-head-size/small-medium/pinkie-fits-sm-med-heads/
- **Leaf category:** `motorcycle-sunglasses → ladies-motorcycle-sunglasses → rhinestones`
- **Situation:** Only product in `rhinestones`. Had multiple categories (ladies, head-size, brand, mirrored) but `rhinestones` was the deepest valid leaf and ended up as a singleton.
- **Action needed:** Owner decides — keep `rhinestones` leaf and add more products, or move Pinkie into `ladies-motorcycle-sunglasses` directly.

---

## Blocker

Owner confirms what to do with each singleton leaf. Once decided, either update the recategorizer's drop/merge map and re-run, or accept the leaf and lower the singleton threshold.
