# Invalid-SKU Product Review

Source: [`migration/reshaped/invalid_sku_products_shape.json`](migration/reshaped/invalid_sku_products_shape.json)

Use this file as our working sheet for products that landed in the invalid-SKU bucket.

For each product, we should capture:
- what it actually is
- whether it should exist in the new site at all
- whether the SKU should be fixed, replaced, or the product handled another way

Suggested action labels:
- `fix-sku` = keep product and assign a valid SKU
- `exclude` = do not migrate
- `convert` = convert into a service/intake/admin flow instead of a normal product
- `ask-owner` = owner decision needed before final handling

## Checklist

- [x] `Try Before You Buy: WileyX 7eye BikerArmour`
- [x] `Rx Option:  BikerArmour Frames`
- [x] `Rx Option: New Frame`
- [x] `Rx Option: XtrActive Transition - Clear to Brown`
- [x] `7eye Replacement Foam`
- [x] `7 Eye Replacement Foam`
- [x] `Prism Custom Fee`
- [x] `Wiley X T-Peg Elastic Strap`
- [x] `Wiley X Cleaning Cloth`
- [x] `Miscellaneous Sunglass Part (Screw, Nose Piece, Rubber Piece)`
- [x] `Rx Digital Sport Progressive Lens`
- [x] `Expedited Shipping`
- [x] `Miscellaneous Sunglass Part`
- [x] `Space Shield Clear Face Mask.  Include Bottle of Spray Cleaner`
- [x] `Rx Option: 50% Off Frame Replacement`
- [x] `2 PACK Bandannas (You get 2 pieces of color you choose! BLACK, HOT PINK, RED, NAVY BLUE, ROYAL BLUE, w/ Yellow Lens in stock!`
- [x] `Biker Armour Protection Kit`
- [x] `Blank Microfiber Cleaning Case`
- [x] `Biker Armour Microfiber Cleaning Case`
- [x] `Padded Sunglasss Case With Zipper With Belt Loop Clip And Carrying Clip`
- [x] `Sunglass String`
- [x] `Zipper Case Medium Size`

## Review Table

| # | Name | Product ID | Current SKU | Variations | What it is | Decision | Action / Notes |
|---|---|---:|---|---:|---|---|---|
| 1 | Try Before You Buy: WileyX 7eye BikerArmour | `69622` | `Try Before You Buy Phone Order` | 0 | Try-before-you-buy form/workflow | Ask-owner | Run by owner to see if they still support this and want it implemented on the new site. |
| 2 | Rx Option:  BikerArmour Frames | `67938` | `None` | 0 | RX option / add-on style item | Ask-owner | Missing SKU and image. Run by owner; likely removable if it no longer serves a clear purpose in the new site. |
| 3 | Rx Option: New Frame | `67933` | `None` | 0 | RX option / add-on style item | Ask-owner | No image and sold out/out of stock. Run by owner; likely a quick throwout if it no longer serves a purpose. |
| 4 | Rx Option: XtrActive Transition - Clear to Brown | `66721` | `None` | 0 | RX option / add-on, not a standalone product | Exclude | No image and not a real standalone product. Do not migrate as a product. |
| 5 | 7eye Replacement Foam | `62720` | `None` | 0 | RX option / add-on, not a standalone product | Exclude | Same as previous style of RX option/add-on item. Do not migrate as a standalone product. |
| 6 | 7 Eye Replacement Foam | `62495` | `None` | 18 | Real replacement-part product | Ask-owner | Foam replacement product with no parent image and missing SKU. Talk to owner and figure out how they want to handle it. |
| 7 | Prism Custom Fee | `62217` | `None` | 0 | Unclear fee/add-on item | Ask-owner | No clear purpose from the page, no image, and missing SKU. Talk to owner and clarify what this is before deciding anything. |
| 8 | Wiley X T-Peg Elastic Strap | `59257` | `WX TPEG-STRAP` | 0 | Real physical product | Ask-owner | Important item. SKU may only need cleanup because of the space, but confirm the intended canonical SKU with the owner. |
| 9 | Wiley X Cleaning Cloth | `59260` | `WX-MF CLOTH` | 0 | Real physical product | Ask-owner | Important item. SKU may only need cleanup because of the space, but confirm the intended canonical SKU with the owner. |
| 10 | Miscellaneous Sunglass Part (Screw, Nose Piece, Rubber Piece) | `58866` | `MISC Sunglass part-1` | 0 | Real accessory/service-style item | Ask-owner | Same as the last important items. Talk to owner and confirm intended handling plus a cleaned canonical SKU. |
| 11 | Rx Digital Sport Progressive Lens | `58688` | `Rx &#8211; Digital Sport Progressive Lens` | 0 | RX lens/add-on style item | Ask-owner | Same as the majority of these RX add-on items. Weird SKU; talk to owner and confirm whether it should exist as a product plus what the canonical SKU should be. |
| 12 | Expedited Shipping | `57740` | `None` | 3 | Shipping workflow/service item | Ask-owner | Shipping item with options. Talk to owner and confirm whether they still want this workflow/product in the new site. |
| 13 | Miscellaneous Sunglass Part | `57737` | `MISC Sunglass part` | 0 | Real accessory/service-style item | Ask-owner | Same as the other misc sunglass part item. Talk to owner, confirm intended handling/cleaned SKU, and note the image appears wrong because it shows glasses rather than sunglasses. |
| 14 | Space Shield Clear Face Mask.  Include Bottle of Spray Cleaner | `54132` | `None` | 0 | Real physical product | Ask-owner | Important real product with reviews, images, and pricing, but missing a SKU. Talk to owner and confirm the canonical SKU before migration. |
| 15 | Rx Option: 50% Off Frame Replacement | `50441` | `None` | 0 | RX replacement form/workflow | Ask-owner | Form-based item. Title appears misleading because the sale is not actually 50% off. Run by owner and clarify whether this flow should stay plus how it should be named. |
| 16 | 2 PACK Bandannas (You get 2 pieces of color you choose! BLACK, HOT PINK, RED, NAVY BLUE, ROYAL BLUE, w/ Yellow Lens in stock! | `49900` | `None` | 13 | Real physical product | Ask-owner | Important real product that is just missing a SKU. Run by owner and confirm the canonical SKU before migration. |
| 17 | Biker Armour Protection Kit | `8722` | `Biker Armour Protection Kit` | 0 | Real physical product | Ask-owner | Important product. Dirty SKU and currently sold out/out of stock, so confirm the canonical SKU and whether it should remain unavailable or return for sale. |
| 18 | Blank Microfiber Cleaning Case | `8716` | `Blank MF` | 6 | Real physical product | Ask-owner | Important product. Dirty/abbreviated SKU with spaces, so confirm the canonical SKU before migration. |
| 19 | Biker Armour Microfiber Cleaning Case | `8711` | `Biker Armour MF` | 2 | Real physical product | Ask-owner | Important product. Dirty/abbreviated SKU with spaces, so confirm the canonical SKU before migration. |
| 20 | Padded Sunglasss Case With Zipper With Belt Loop Clip And Carrying Clip | `8694` | `Zipper Case Deep` | 0 | Real physical product | Ask-owner | Important product. Current SKU may be usable but title/metadata need sanity check, and it is currently sold out/out of stock. |
| 21 | Sunglass String | `8709` | `Sunglass Strap` | 0 | Real physical product | Ask-owner | Important product. Current SKU reads more like the product name than a clean canonical SKU, so confirm it with the owner before migration. |
| 22 | Zipper Case Medium Size | `8689` | `Zipper Case Medium` | 0 | Real physical product | Ask-owner | Important product. Current SKU reads like the product name rather than a clean canonical SKU, so confirm it with the owner before migration. |

## Per-Product Notes

### 1. Try Before You Buy: WileyX 7eye BikerArmour
- Product ID: `69622`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/brands/try-before-you-buy-wileyx-7eye-bikerarmou/`
- Current SKU: `Try Before You Buy Phone Order`
- Initial signal: invalid SKU because it contains spaces and reads more like an internal label than a product SKU
- What it is: A try-before-you-buy form/workflow where the customer appears to get frames shipped for evaluation.
- Decision: `ask-owner`
- Action / Notes: 100% run by owner to confirm whether this program is still supported and should be implemented on the new site. If kept, it likely should not remain a normal catalog product with this SKU shape.

### 2. Rx Option:  BikerArmour Frames
- Product ID: `67938`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/brands/rx-option-bikerarmour-frames/`
- Current SKU: `None`
- Initial signal: missing SKU and image, and the name reads more like an internal RX option/add-on than a standalone product
- What it is: An RX option/add-on style item rather than a normal well-formed catalog product.
- Decision: `ask-owner`
- Action / Notes: Run by owner. Missing SKU and image, and likely something we can get rid of if it no longer serves a clear purpose in the new site.

### 3. Rx Option: New Frame
- Product ID: `67933`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/bikerarmour-rx-frames/bikerarmour-for-rx-new/`
- Current SKU: `None`
- Initial signal: missing SKU, no image, sold out/out of stock, and reads more like an internal RX option/add-on than a standalone product
- What it is: An RX option/add-on style item rather than a normal well-formed catalog product.
- Decision: `ask-owner`
- Action / Notes: Run by owner. No image and sold out/out of stock, so this is likely a quick throwout if it no longer serves a real purpose in the new site.

### 4. Rx Option: XtrActive Transition - Clear to Brown
- Product ID: `66721`
- `wpUrl`: `https://bikershades.com/shop/motorcycle-sunglasses/brands/rx-option-xtractive-transition-clear-to-brown/`
- Current SKU: `None`
- Initial signal: missing SKU, no image, and reads like an RX add-on rather than a standalone product
- What it is: An RX option/add-on, not a real standalone product.
- Decision: `exclude`
- Action / Notes: No image and not a real product. Do not migrate this as a standalone product.

### 5. 7eye Replacement Foam
- Product ID: `62720`
- `wpUrl`: `https://bikershades.com/shop/all-products/rx-option-7-eye-replacement-foam-2/`
- Current SKU: `None`
- Initial signal: missing SKU, no image, and reads like an RX add-on / replacement-part option rather than a standalone product
- What it is: An RX option/add-on, not a real standalone product.
- Decision: `exclude`
- Action / Notes: Same as the previous type of RX option/add-on item. Do not migrate this as a standalone product.

### 6. 7 Eye Replacement Foam
- Product ID: `62495`
- `wpUrl`: `https://bikershades.com/shop/accessories/extra-lenses/rx-option-7-eye-replacement-foam/`
- Current SKU: `None`
- Initial signal: missing SKU and no parent image, but unlike the prior duplicate entry this one looks like the actual replacement-foam product with variations
- What it is: A real replacement-part product.
- Decision: `ask-owner`
- Action / Notes: Foam replacement product with no parent image and missing SKU. Talk to owner and figure out whether to keep it, what the canonical SKU should be, and whether a proper parent image should be added.

### 7. Prism Custom Fee
- Product ID: `62217`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/rx-brands/prism-custom-fee/`
- Current SKU: `None`
- Initial signal: missing SKU, no image, and unclear purpose from the product page/name
- What it is: Unclear fee/add-on item.
- Decision: `ask-owner`
- Action / Notes: No idea what this is from the current page alone. Talk to owner and clarify its purpose before deciding whether to keep, exclude, or fold it into some other workflow.

### 8. Wiley X T-Peg Elastic Strap
- Product ID: `59257`
- `wpUrl`: `https://bikershades.com/shop/accessories/wiley-x-t-peg-elastic-strap/`
- Current SKU: `WX TPEG-STRAP`
- Initial signal: invalid SKU because it contains a space, but otherwise looks like a real product with usable product data
- What it is: A real physical accessory product.
- Decision: `ask-owner`
- Action / Notes: Important item. The SKU may just need cleanup rather than replacement, so talk to owner and confirm the intended canonical SKU format/value before migration.

### 9. Wiley X Cleaning Cloth
- Product ID: `59260`
- `wpUrl`: `https://bikershades.com/shop/accessories/wiley-x-cleaning-cloth/`
- Current SKU: `WX-MF CLOTH`
- Initial signal: invalid SKU because it contains a space, but otherwise looks like a real product with usable product data
- What it is: A real physical accessory product.
- Decision: `ask-owner`
- Action / Notes: Exact same situation as the T-Peg elastic strap. Important item. The SKU may just need cleanup rather than replacement, so talk to owner and confirm the intended canonical SKU format/value before migration.

### 10. Miscellaneous Sunglass Part (Screw, Nose Piece, Rubber Piece)
- Product ID: `58866`
- `wpUrl`: `https://bikershades.com/shop/accessories/tools/miscellaneous-sunglass-part-screw-nose-piece-rubber-piece/`
- Current SKU: `MISC Sunglass part-1`
- Initial signal: invalid SKU because it contains spaces, but otherwise looks like a real item/workflow that customers may still use
- What it is: A real accessory/service-style item for ordering miscellaneous sunglass parts.
- Decision: `ask-owner`
- Action / Notes: Same as the last important items. TALK TO OWNER. Confirm whether they still want this workflow and what the cleaned canonical SKU should be if it stays.

### 11. Rx Digital Sport Progressive Lens
- Product ID: `58688`
- `wpUrl`: `https://bikershades.com/shop/all-products/rx-digital-sport-progressive-lens/`
- Current SKU: `Rx &#8211; Digital Sport Progressive Lens`
- Initial signal: invalid/weird SKU with HTML entity encoding and product-name-like text instead of a clean SKU
- What it is: An RX lens/add-on style item rather than a normal cleanly-modeled product.
- Decision: `ask-owner`
- Action / Notes: Same as the majority of these RX option/add-on items. Talk to owner and confirm whether it should exist as a product at all and, if so, what the cleaned canonical SKU should be.

### 12. Expedited Shipping
- Product ID: `57740`
- `wpUrl`: `https://bikershades.com/shop/accessories/return-labels/expedited-shipping/`
- Current SKU: `None`
- Initial signal: missing SKU, but this is clearly a shipping workflow/service item with selectable shipping options
- What it is: A shipping workflow/service item rather than a normal physical product.
- Decision: `ask-owner`
- Action / Notes: Talk to owner and confirm whether they still want this expedited shipping workflow represented in the new site.

### 13. Miscellaneous Sunglass Part
- Product ID: `57737`
- `wpUrl`: `https://bikershades.com/shop/accessories/tools/miscellaneous-sunglass-part/`
- Current SKU: `MISC Sunglass part`
- Initial signal: invalid SKU because it contains spaces, and the image appears mismatched for a sunglass-part listing
- What it is: A real accessory/service-style item for ordering miscellaneous sunglass parts.
- Decision: `ask-owner`
- Action / Notes: Same as the other misc sunglass part item. Talk to owner and confirm intended handling plus a cleaned canonical SKU. Also note the image looks wrong because it shows glasses rather than sunglasses.

### 14. Space Shield Clear Face Mask.  Include Bottle of Spray Cleaner
- Product ID: `54132`
- `wpUrl`: `https://bikershades.com/shop/accessories/safety-protection/space-shield-clear-face-mask-include-bottle-of-spray-cleaner/`
- Current SKU: `None`
- Initial signal: missing SKU, but otherwise looks like a real product with images, pricing, and at least one review
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration, since this looks like a legitimate product that should not be dropped casually.

### 15. Rx Option: 50% Off Frame Replacement
- Product ID: `50441`
- `wpUrl`: `https://bikershades.com/shop/prescription-motorcycle-glasses/50-off-rx-frame-replacement/`
- Current SKU: `None`
- Initial signal: missing SKU, form-based flow, and title/pricing look inconsistent with the claimed “50% Off”
- What it is: An RX replacement form/workflow rather than a clean standalone product.
- Decision: `ask-owner`
- Action / Notes: Run by owner. The title looks wrong because the sale shown is not actually 50% off, so confirm whether this flow should stay and what the correct naming/pricing story should be.

### 16. 2 PACK Bandannas (You get 2 pieces of color you choose! BLACK, HOT PINK, RED, NAVY BLUE, ROYAL BLUE, w/ Yellow Lens in stock!
- Product ID: `49900`
- `wpUrl`: `https://bikershades.com/shop/accessories/safety-protection/2-pack-bandannas-you-get-2-pieces-of-color-you-choose/`
- Current SKU: `None`
- Initial signal: missing SKU, but otherwise clearly a real product with images, options, and pricing
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Just missing a SKU, so run by owner and confirm the canonical SKU before migration.

### 17. Biker Armour Protection Kit
- Product ID: `8722`
- `wpUrl`: `https://bikershades.com/shop/accessories/cases/biker-armour-protection-kit/`
- Current SKU: `Biker Armour Protection Kit`
- Initial signal: invalid SKU because it contains spaces and reads like a product title; also currently sold out/out of stock
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration, and also confirm whether it should remain unavailable or return for sale.

### 18. Blank Microfiber Cleaning Case
- Product ID: `8716`
- `wpUrl`: `https://bikershades.com/shop/accessories/cases/blank-microfiber-cleaning-case/`
- Current SKU: `Blank MF`
- Initial signal: invalid SKU because it contains spaces and uses an abbreviated/internal-looking format
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration.

### 19. Biker Armour Microfiber Cleaning Case
- Product ID: `8711`
- `wpUrl`: `https://bikershades.com/shop/accessories/cases/biker-armour-microfiber-cleaning-case/`
- Current SKU: `Biker Armour MF`
- Initial signal: invalid SKU because it contains spaces and uses an abbreviated/internal-looking format
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration.

### 20. Padded Sunglasss Case With Zipper With Belt Loop Clip And Carrying Clip
- Product ID: `8694`
- `wpUrl`: `https://bikershades.com/shop/accessories/cases/padded-sunglasss-case-with-zipper-with-belt-loop-clip-and-carrying-clip/`
- Current SKU: `Zipper Case Deep`
- Initial signal: current SKU is not the full product name, but both the title and SKU need sanity-checking because the naming is messy and the product is sold out/out of stock
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration, and also confirm whether it should remain unavailable or return for sale.

### 21. Sunglass String
- Product ID: `8709`
- `wpUrl`: `https://bikershades.com/shop/accessories/strings/sunglass-string/`
- Current SKU: `Sunglass Strap`
- Initial signal: current SKU reads more like a product name/label than a clean canonical SKU
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration.

### 22. Zipper Case Medium Size
- Product ID: `8689`
- `wpUrl`: `https://bikershades.com/shop/accessories/cases/zipper-case-medium-size/`
- Current SKU: `Zipper Case Medium`
- Initial signal: current SKU reads more like the product name than a clean canonical SKU
- What it is: A real physical product.
- Decision: `ask-owner`
- Action / Notes: Important item. Talk to owner and confirm the canonical SKU before migration.
