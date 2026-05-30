# No-Weight Product Review

Source: [`migration/reshaped/no_weight_products_shape.json`](migration/reshaped/no_weight_products_shape.json)

Use this file as our working sheet for products that landed in the no-weight bucket.

For each product, we should capture:
- what it actually is
- whether weight is truly required for the new site
- whether we should add a default weight, exclude it, or handle it differently

Suggested action labels:
- `add-weight` = keep product and assign/fix weight
- `no-weight-ok` = keep product and allow no weight because shipping logic does not need it
- `exclude` = do not migrate
- `convert` = convert into a service/intake/admin flow instead of a normal product
- `ask-owner` = owner decision needed before final handling

## Checklist

- [x] `Return USPS Shipping Label with Insurance (more than 2 pairs)`
- [x] `1 Year NON Prescription Sunglass Warranty`
- [x] `USPS First Class Shipping`
- [x] `Wiley X XL-1 Advanced for Rx [SM - MED]`
- [x] `Wiley X Leash Cord Strap`
- [x] `Wiley X Clamshell Hard Zipper Case`
- [x] `Return USPS Shipping Label with Insurance`
- [x] `Dynamo Combos [Fits LG-XL Heads]`
- [x] `Dragster 2 PAIR COMBOS [Fits MED-XL Heads]`
- [x] `Cobra COMBOS [Fits SM - MED Heads]`
- [x] `Wiley X Romer3 for Eclipse XT [MED - LG]`
- [x] `BikerArmour Pola Bora for Eclipse XT [SM - MED]`

## Review Table

| # | Name | Product ID | SKU | Variations | What it is | Decision | Action / Notes |
|---|---|---:|---|---:|---|---|---|
| 1 | Return USPS Shipping Label with Insurance (more than 2 pairs) | `66714` | `LABEL-USPSRETURN-2` | 0 | Return-label service item | Ask-owner | Run by owner to see if they want this workflow/product in the new site. Not a normal physical product, so missing weight is likely acceptable if retained. |
| 2 | 1 Year NON Prescription Sunglass Warranty | `62556` | `LABEL-USPSRETURN-1-1` | 5 | Warranty service item with tiered plans | Ask-owner | Run by owner to see if they want this warranty workflow in the new site. Not a normal physical product, so missing weight is likely acceptable if retained. |
| 3 | USPS First Class Shipping | `62489` | `LABEL-USPSRETURN-1` | 0 | Shipping service item | Ask-owner | Run by owner to see if they want this workflow/product in the new site. Not a normal physical product, so missing weight is likely acceptable if retained. |
| 4 | Wiley X XL-1 Advanced for Rx [SM - MED] | `59334` | `WX-XL1-RX` | 0 | Rx product with multipart form/configuration flow | Ask-owner | Real product, but it uses a form/configurator and is missing weight. Run by owner and confirm how they want Rx form products handled on the new site. |
| 5 | Wiley X Leash Cord Strap | `59262` | `WXSTRAP` | 0 | Small physical accessory | Ask-owner | Should probably get a low weight if kept. Currently sold out, so confirm with owner whether it should remain unavailable or return for sale. |
| 6 | Wiley X Clamshell Hard Zipper Case | `59254` | `WX-CASE` | 0 | Physical accessory case | Add-weight | Keep in migration. Owner should provide the weight if known/available so shipping data is complete. |
| 7 | Return USPS Shipping Label with Insurance | `57735` | `LABEL-USPSRETURN` | 0 | Return-label service item | Ask-owner | Same as the other return-label product. Run by owner to see if they want this workflow/product in the new site. Missing weight is likely acceptable if retained. |
| 8 | Dynamo Combos [Fits LG-XL Heads] | `54443` | `CFM65X07-0-COMBO` | 4 | Real combo product | Ask-owner | Whole product appears valid; main issue is missing weight. Talk to owner and have them provide/confirm the weight. |
| 9 | Dragster 2 PAIR COMBOS [Fits MED-XL Heads] | `54423` | `CFM48X55DS-0-COMBOS` | 8 | Real combo product | Add-weight | We want to migrate this. Get the weight now so shipping is handled cleanly up front instead of as a later exception. |
| 10 | Cobra COMBOS [Fits SM - MED Heads] | `54403` | `CFM20X02CO-0-COMBO` | 7 | Real combo product | Ask-owner | Product looks valid; main issue is missing weight. Talk to owner and have them provide/confirm the weight. |
| 11 | Wiley X Romer3 for Eclipse XT [MED - LG] | `40711` | `WX-ROMER3-0-XT` | 11 | Real configurable product | Ask-owner | Product looks valid; main issue is missing weight. Talk to owner and have them provide/confirm the weight. |
| 12 | BikerArmour Pola Bora for Eclipse XT [SM - MED] | `3748` | `FM0X75PB-0-XT` | 11 | Real configurable product | Ask-owner | Product looks valid; main issue is missing weight. Talk to owner and have them provide/confirm the weight. |

## Per-Product Notes

### 1. Return USPS Shipping Label with Insurance (more than 2 pairs)
- Product ID: `66714`
- `wpUrl`: `https://bikershades.com/shop/accessories/return-labels/return-usps-shipping-label-with-insurance-more-than-2-pairs/`
- Initial signal: shipping/service line item rather than physical merchandise
- What it is: A return-label service item customers buy so Bikershades can send them a USPS return label with insurance.
- Decision: `ask-owner`
- Action / Notes: Run by owner to see if they want this workflow/product on the new site. This is not a normal physical product, so the missing weight is probably fine if they decide to keep it.

### 2. 1 Year NON Prescription Sunglass Warranty
- Product ID: `62556`
- `wpUrl`: `https://bikershades.com/shop/accessories/return-labels/1-year-non-prescription-sunglass-warranty/`
- Initial signal: warranty/service product with price tiers as variations
- What it is: A warranty service item with multiple plan/price tiers based on the original sunglass purchase price.
- Decision: `ask-owner`
- Action / Notes: Run by owner to see if they want this warranty workflow in the new site. This is not a normal physical product, so the missing weight is probably fine if they decide to keep it.

### 3. USPS First Class Shipping
- Product ID: `62489`
- `wpUrl`: `https://bikershades.com/shop/accessories/return-labels/usps-first-class-shipping/`
- Initial signal: shipping/service line item rather than physical merchandise
- What it is: A shipping service item customers purchase so Bikershades can ship an order or complete a shipping-related workflow.
- Decision: `ask-owner`
- Action / Notes: Run by owner to see if they want this workflow/product in the new site. This is not a normal physical product, so the missing weight is probably fine if they decide to keep it.

### 4. Wiley X XL-1 Advanced for Rx [SM - MED]
- Product ID: `59334`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/wileyx-rx-frames/wiley-x-xl-1-advanced-prescription/`
- Initial signal: Rx product or configuration flow missing weight
- What it is: A real Rx product page with a multipart form/configuration flow.
- Decision: `ask-owner`
- Action / Notes: It is not just missing weight; it is also part of the broader Rx form/configurator pattern. Run by owner and confirm how they want these Rx form products handled on the new site.

### 5. Wiley X Leash Cord Strap
- Product ID: `59262`
- `wpUrl`: `https://bikershades.com/shop/accessories/wiley-x-leash-cord-strap/`
- Initial signal: physical accessory that may simply be missing weight metadata
- What it is: A small physical accessory product.
- Decision: `ask-owner`
- Action / Notes: It should probably have a low weight if kept. The page currently shows it as sold out, so confirm with the owner whether it should remain unavailable or come back for sale.

### 6. Wiley X Clamshell Hard Zipper Case
- Product ID: `59254`
- `wpUrl`: `https://bikershades.com/shop/accessories/wiley-x-clamshell-hard-zipper-case/`
- Initial signal: physical accessory that may simply be missing weight metadata
- What it is: A physical accessory case product.
- Decision: `add-weight`
- Action / Notes: Keep in migration. Missing weight is the main issue here, so the owner should provide the weight if they know it or have the product available to measure.

### 7. Return USPS Shipping Label with Insurance
- Product ID: `57735`
- `wpUrl`: `https://bikershades.com/shop/accessories/return-labels/return-shipping-label/`
- Initial signal: shipping/service line item rather than physical merchandise
- What it is: A return-label service item customers purchase so Bikershades can send them a USPS return label with insurance.
- Decision: `ask-owner`
- Action / Notes: Same as the other return-label product. Run by owner to see if they want this workflow/product in the new site. This is not a normal physical product, so the missing weight is probably fine if they decide to keep it.

### 8. Dynamo Combos [Fits LG-XL Heads]
- Product ID: `54443`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/head-sizes/large-xl-heads/dynamo-fits-lg-xl-heads/`
- Initial signal: real combo product missing weight metadata
- What it is: A real sellable combo product.
- Decision: `ask-owner`
- Action / Notes: Whole product appears valid; the main issue is missing weight. Talk to owner and have them provide or confirm the correct weight for migration.

### 9. Dragster 2 PAIR COMBOS [Fits MED-XL Heads]
- Product ID: `54423`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/head-sizes/medium-xl-heads/dragster-combos-fits-med-xl-heads/`
- Initial signal: real combo product missing weight metadata
- What it is: A real sellable combo product.
- Decision: `add-weight`
- Action / Notes: We want to migrate this. Get the weight now so shipping is handled cleanly up front instead of dealing with this later as a one-off exception when the item comes up.

### 10. Cobra COMBOS [Fits SM - MED Heads]
- Product ID: `54403`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/head-sizes/sm-med-heads/cobra-combos-fits-sm-med-heads/`
- Initial signal: real combo product missing weight metadata
- What it is: A real sellable combo product.
- Decision: `ask-owner`
- Action / Notes: Product looks valid; the main issue is missing weight. Talk to owner and have them provide or confirm the correct weight for migration.

### 11. Wiley X Romer3 for Eclipse XT [MED - LG]
- Product ID: `40711`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/wileyx-rx-frames/wiley-x-romer-3-for-eclipse-xt/`
- Initial signal: configurable Rx product missing weight metadata
- What it is: A real sellable configurable product.
- Decision: `ask-owner`
- Action / Notes: Product looks valid; the main issue is missing weight. Talk to owner and have them provide or confirm the correct weight for migration.

### 12. BikerArmour Pola Bora for Eclipse XT [SM - MED]
- Product ID: `3748`
- `wpUrl`: `https://bikershades.com/shop/transitions/sunglasses-with-rx-insert/pola-bora-for-eclipse-xt/`
- Initial signal: configurable product missing weight metadata
- What it is: A real sellable configurable product.
- Decision: `ask-owner`
- Action / Notes: Product looks valid; the main issue is missing weight. Talk to owner and have them provide or confirm the correct weight for migration.
