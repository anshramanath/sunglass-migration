# Zero-Price Product Review

Source: [`migration/reshaped/zero_price_products_shape.json`](migration/reshaped/zero_price_products_shape.json)

Use this file as our working sheet. For each product, we should capture:
- what it actually is
- whether it belongs in the new catalog
- what action we want to take

Current overall takeaway:
- Every zero-price item should be reviewed with the owner before final migration decisions.
- `Distributor Invoice` is still the clearest default `exclude`, but we can still confirm with the owner in case it relates to an internal workflow they care about.

Suggested action labels:
- `keep` = keep as a real catalog product
- `exclude` = do not migrate
- `needs-price` = real product, but pricing must be fixed
- `convert` = convert into a service/intake flow instead of a normal product
- `merge` = merge into another product or flow

## Checklist

- [x] `Distributor Invoice`
- [x] `Got Your Own Frame?`
- [x] `Panther`
- [x] `Wiley X Saint for Rx [SM - LG]`
- [x] `Ziena Kai Dry-Eye Glasses For RX (FITS SMALL HEADS)`
- [x] `Sahara Dark Polarized`
- [x] `Robin Goggle for Rx [Fits XXS-SM]`
- [x] `CUSTOM PRESCRIPTION LENSES FOR YOUR FRAMES`

## Review Table

| # | Name | SKU | Slug | What it is | Decision | Action / Notes |
|---|---|---|---|---|---|---|
| 1 | Distributor Invoice |  | `distributor-invoice` | Empty placeholder page / non-product artifact | Exclude | Remove from migration. No SKU, no categories, no images, and page content is effectively blank. |
| 2 | Got Your Own Frame? |  | `got-your-own-frame` | Dynamic custom Rx intake form for customer-owned frames | Exclude | Do not migrate as a catalog product. Revisit later with owner to decide whether this flow should exist in the new site. Preserve WP URL as reference. |
| 3 | Panther | `CA51X57PT-BK-YL` | `panther` | Real catalog product | Needs-price | Keep in migration, but pricing must be restored/fixed before import. |
| 4 | Wiley X Saint for Rx [SM - LG] | `WX-SAINT-0-XT-1` | `wiley-x-saint-for-rx-sm-lg` | Multipart Rx configuration and ordering flow | Convert | Do not migrate as a normal fixed-price product yet. Talk to owner about whether to rebuild this configurator/workflow on the new site. |
| 5 | Ziena Kai Dry-Eye Glasses For RX (FITS SMALL HEADS) | `7EYE-KAI-RX` | `ziena-kai-dry-eye-prescription-glasses` | Multipart Rx configuration and ordering flow | Convert | Do not migrate as a normal fixed-price product yet. Talk to owner about whether to rebuild this configurator/workflow on the new site. |
| 6 | Sahara Dark Polarized | `SPPL80X59SH-Dark-0` | `sahara-polarized` | Real catalog product, currently unavailable/out of stock | Needs-price | Ask owner whether it should stay unavailable or return for sale, and whether price is intentionally hidden until availability returns. |
| 7 | Robin Goggle for Rx [Fits XXS-SM] | `GO47X11RB-RX` | `robin-goggle-for-rx-fits-kids-xs-heads` | Rx product page with no visible price or form | Convert | Talk to owner before migration. Need to confirm whether this should be sold, rebuilt as an Rx flow, or excluded. |
| 8 | CUSTOM PRESCRIPTION LENSES FOR YOUR FRAMES | `CUSTOMPRESCRIPTIONGOTFRAME` | `custom-prescription-lenses-for-your-frames-3` | Multipart custom Rx intake and ordering flow | Convert | Same pattern as the other form-based Rx flows. Do not migrate as a normal fixed-price product yet; confirm with owner whether to rebuild this workflow. |

## Per-Product Notes

### 1. Distributor Invoice
- Product ID: `69167`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/brands/distributor-invoice/`
- Initial signal: no SKU, no categories, no images
- What it is: Empty placeholder page or internal artifact, not a real sellable product.
- Decision: `exclude`
- Action / Notes: Default recommendation is to remove from migration. Still worth confirming with the owner once in case this slug relates to an internal billing/invoice workflow they want preserved elsewhere.

### 2. Got Your Own Frame?
- Product ID: `68423`
- `wpUrl`: `https://bikershades.com/shop/got-frames/got-your-own-frame/`
- Initial signal: looks like a service / intake product
- What it is: A dynamic multi-step custom prescription intake flow for customer-owned frames, not a standard catalog product.
- Decision: `exclude`
- Action / Notes: Do not migrate as a product by default. Keep the WP URL above so we can revisit the original flow if the owner wants this feature rebuilt later. Needs owner review before finalizing.

### 3. Panther
- Product ID: `67150`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/lens-type/yellow/panther/`
- Initial signal: looks like a real catalog product with missing or broken pricing
- What it is: A real sellable sunglasses product page.
- Decision: `needs-price`
- Action / Notes: Keep in migration by default. The only blocker is missing pricing, so we should recover or confirm the intended price before import. Needs owner review.

### 4. Wiley X Saint for Rx [SM - LG]
- Product ID: `66081`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/wiley-x-saint-for-rx-sm-lg/`
- Initial signal: looks like a real RX frame product with missing or deferred pricing
- What it is: A real Rx product page, but purchase happens through a multipart configuration form and the final price is calculated from the chosen options.
- Decision: `convert`
- Action / Notes: Do not migrate as a standard catalog product for now. Revisit with the owner to confirm whether this Rx configurator should be rebuilt in the new site and, if so, whether it should be a product page, guided form, or separate quote/order flow.

### 5. Ziena Kai Dry-Eye Glasses For RX (FITS SMALL HEADS)
- Product ID: `59727`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/ziena-kai-dry-eye-prescription-glasses/`
- Initial signal: looks like a real RX frame product with missing or deferred pricing
- What it is: A real Rx product page, but checkout happens through a multipart configuration form and the final price is calculated from the selected options.
- Decision: `convert`
- Action / Notes: Treat the same as the Wiley X Saint flow. Do not migrate as a standard catalog product for now. Revisit with the owner to confirm whether this Rx configurator should be rebuilt in the new site and what the right experience should be.

### 6. Sahara Dark Polarized
- Product ID: `51841`
- `wpUrl`: `https://bikershades.com/shop/polarized-motorcycle-sunglasses/sahara-polarized/`
- Initial signal: looks like a real catalog product with missing or broken pricing
- What it is: A real sellable sunglasses product page that is currently marked out of stock and unavailable.
- Decision: `needs-price`
- Action / Notes: Ask the owner whether this product should stay unavailable or return for sale, and whether the price is intentionally hidden while out of stock.

### 7. Robin Goggle for Rx [Fits XXS-SM]
- Product ID: `51507`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/see-all-rx-frames/robin-goggle-for-rx-fits-kids-xs-heads/`
- Initial signal: looks like a real RX frame product with missing or deferred pricing
- What it is: An Rx product page, but there is no visible price and no visible multipart ordering form on the current page.
- Decision: `convert`
- Action / Notes: Talk to owner before migration. We need to confirm whether this product should still be sold, whether a missing Rx flow needs to be rebuilt, or whether it should be excluded from the new site.

### 8. CUSTOM PRESCRIPTION LENSES FOR YOUR FRAMES
- Product ID: `12601`
- `wpUrl`: `https://bikershades.com/shop/got-frames/custom-prescription-lenses-for-your-frames-3/`
- Initial signal: likely service / intake flow rather than a normal product
- What it is: A multipart custom Rx intake/order flow for customer-provided frames, with pricing determined through the form selections.
- Decision: `convert`
- Action / Notes: Same pattern as the other form-based Rx products. Do not migrate as a standard catalog product for now. Revisit with the owner to confirm whether this workflow should be rebuilt in the new site and how it should be represented.
