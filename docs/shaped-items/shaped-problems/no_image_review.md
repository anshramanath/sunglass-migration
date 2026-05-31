# No-Image Product Review

Source: [`migration/reshaped/no_image_products_shape.json`](migration/reshaped/no_image_products_shape.json)

Use this file as our working sheet for products that landed in the no-image bucket.

For each product, we should capture:
- what it actually is
- whether the product truly has no usable image
- whether images exist at the variation level only
- whether we should source/add images, exclude it, or handle it another way

Suggested action labels:
- `add-image` = keep product and add/fix product-level images
- `variation-images-ok` = keep product and rely on variation images if that fits the new site
- `exclude` = do not migrate
- `ask-owner` = owner decision needed before final handling

## Checklist

- [x] `Wiley X Replacement Foam Seal`
- [x] `7 Eye Replacement Eyecup`
- [x] `Angel Rhinestones for Ladies COMBOS [Fits MED - LG Heads]`

## Review Table

| # | Name | Product ID | SKU | Variations | What it is | Decision | Action / Notes |
|---|---|---:|---|---:|---|---|---|
| 1 | Wiley X Replacement Foam Seal | `61243` | `WX-EYECUP` | 0 | Replacement-part service/product | Ask-owner | Talk to owner and try to get a real image. If no image is available, only use a placeholder with owner approval. |
| 2 | 7 Eye Replacement Eyecup | `61059` | `7EYE-EYECUP` | 0 | Replacement-part service/product | Ask-owner | Same as the Wiley X foam seal item. Talk to owner and try to get a real image; only use a placeholder with owner approval. |
| 3 | Angel Rhinestones for Ladies COMBOS [Fits MED - LG Heads] | `54632` | `CFM85X11MNRS-0-COMBOS` | 16 | Real combo product with broken/stale missing images | Ask-owner | Run by owner to see if they still have usable images. Looks like images may have existed before and gone stale/broken. |

## Per-Product Notes

### 1. Wiley X Replacement Foam Seal
- Product ID: `61243`
- `wpUrl`: `https://bikershades.com/shop/accessories/tools/wileyx-replacement-foam-seal/`
- Initial signal: product exists but has no product-level image in source data
- What it is: A replacement-part service/product where the customer checks out and specifies the foam seal style they need.
- Decision: `ask-owner`
- Action / Notes: Talk to owner and try to get a real image. If no image is available, only use a placeholder if they explicitly approve that fallback.

### 2. 7 Eye Replacement Eyecup
- Product ID: `61059`
- `wpUrl`: `https://bikershades.com/shop/accessories/tools/7-eye-replacement-eyecup/`
- Initial signal: product exists but has no product-level image in source data
- What it is: A replacement-part service/product where the customer checks out and specifies the eyecup style they need.
- Decision: `ask-owner`
- Action / Notes: Same as the Wiley X foam seal item. Talk to owner and try to get a real image; only use a placeholder if they explicitly approve that fallback.

### 3. Angel Rhinestones for Ladies COMBOS [Fits MED - LG Heads]
- Product ID: `54632`
- `wpUrl`: `https://bikershades.com/shop/all-products/angel-for-ladies-combos-fits-med-lg-heads-w-rhinestones/`
- Initial signal: no parent product images, but review whether variation images exist / are enough
- What it is: A real combo product, but images appear missing across the product and variations.
- Decision: `ask-owner`
- Action / Notes: Run by owner to see if they still have usable images. This looks like a stale/broken image situation rather than an intentionally imageless product.
