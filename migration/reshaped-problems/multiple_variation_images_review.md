# Multiple Variation Images Review
_Last updated: 2026-05-31_

**Source:** `migration/reshaped/multiple_variation_images_items.json`

One product has variations where each variation has more than 1 image. Variations are expected to have at most 1 image — we store `image_src` and `image_name` inline on the variation row. More than 1 is a WooCommerce misconfiguration.

---

## Product

| SKU | Name | WpUrl |
|-----|------|-------|
| `WX-BOSS-0-XT` | Wiley X Boss for Eclipse XT [MED – LG] | https://bikershades.com/shop/transitions-motorcycle-sunglasses/transition-motorcycle-sunglasses-eclipse-xt/eclipse_xt_transition_motorcycle_sunglasses_wileyx/wiley-x-boss-for-eclipse-xt-motorcycle-transition-glasses/ |

---

## Problem

Multiple variations all have the same 3 images attached:
- `BOSS-CLEAR-LENS-MATTE-BLACK-FRAME.jpg`
- `BOSS-GREY-SILVER-FLASH-LENS-GLOSS-BLACK-FRAME.jpg`
- `BOSS-POL-VENICE-GOLD-MIRROR-KRYPTEK-HIGHLANDER-FRAME.jpg`

These images belong at the **product level**, not the variation level. They appear to have been accidentally attached to every variation rather than set as product gallery images.

---

## Decision

**Ask owner** — confirm which image (if any) is the correct per-variation image. Most likely the fix is to move all 3 to the product gallery and clear variation images, or assign one specific image per variation based on color.

---

## Blocker

Owner confirms which image corresponds to each variation, or confirms all 3 should be product gallery images only.
