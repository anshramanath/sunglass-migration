# Product Funnel — WooCommerce → create_items
_Pipeline: fetch → slim → validate_products → fetch_variations → slim_variations → validate_variations → reshape → create_items_
_Updated: 2026-06-05_

---

## Validation rules

**Simple products** are flagged if:
1. SKU not in Veeqo
2. SKU has no NNXnn model number (digits + X + digits)

**Variations** are flagged if:
1. SKU not in Veeqo
2. SKU has no NNXnn model number
3. Has NNXnn but it differs from siblings in the same product (model mismatch)

Variable products pass or fail at validate_products unconditionally — only their variations are gated. A variable product is dropped at create_items if it ends up with no filled variations after gating.

---

## Summary

| Stage | ProSport | Monster | BikerShades |
|---|---|---|---|
| Fetched products | 171 | 277 | 704 |
| Validated products | 165 (-6) | 268 (-9) | 541 (-163) |
| Fetched variations | 1,794 | 2,796 | 6,165 |
| Validated variations | 1,519 (-275) | 2,591 (-205) | 4,425 (-1,740) |
| **create_items passed** | **148 (-17)** | **243 (-25)** | **401 (-140)** |
| Variations embedded | 1,505 | 2,499 | 4,383 |

---

## ProSport

### validate_products — 171 → 165 passed, 6 flagged

| Product | Reasons |
|---|---|
| Sunglass String Chum Strap | not in Veeqo + no model |
| Ruby Extra Large Zipper Case | no model |
| Diamond Chrome Hard Case | no model |
| Sunglasses Repair Kit | no model |
| Sunglasses Repair Screw Driver | no model |
| Sunglasses Lens Cleaner | no model |

All accessories/non-product simple products.

### validate_variations — 1,794 → 1,519 passed, 275 flagged

| Reason | Count |
|---|---|
| Not in Veeqo | ~240 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 24 |
| No NNXnn model | ~10 |
| Model mismatch: FLPL7X59SB vs FLPL73X31SB (Sharkbait Float) | 3 |
| Model mismatch: CA10X15CP vs CA10X16CP (Chipper) | 4 |

Not-in-Veeqo covers the full variation sets for: Cabriolet Mirror Bifocal (Copy) (36), Verbena (45), Bypass Bifocal (36), Gullwing Bifocal (44), Eliminator Polarized Bifocal (16), Iris Bifocal (12), Brooklyn Reader (18), Cooper Polarized Bifocal (8), Cooper Bifocal (12), and partial sets for Sharkbait Polarized Bifocal (7) and Sharkbait Polarized Float (3).

### create_items — 165 → 148 passed, 17 flagged

| Product | Flag |
|---|---|
| Cabriolet Mirror Bifocal (Copy) | no filled variations (all not in Veeqo) |
| Verbena Sunglass Readers | no filled variations (all not in Veeqo) |
| Bypass Bifocal | no filled variations (all not in Veeqo) |
| Gullwing Bifocal | no filled variations (all not in Veeqo) |
| Eliminator Polarized Bifocal | no filled variations (all not in Veeqo) |
| Iris Bifocal | no filled variations (all not in Veeqo) |
| Brooklyn Reader | no filled variations (all not in Veeqo) |
| Cooper Polarized Bifocal | no filled variations (all not in Veeqo) |
| Cooper Bifocal | no filled variations (all not in Veeqo) |
| Sharkbait Polarized Float Sunglasses | no filled variations (model mismatch) |
| Chipper Aviator Sunglasses | no filled variations (model mismatch) |
| Kumatage Bifocal | no filled variations (model mismatch) |
| Altitude Polarized Leather Shield | no filled variations (no NNXnn) |
| Leopard Print Hard Case | no filled variations (no NNXnn) |
| Jade Deep Fabric Case | no filled variations (no NNXnn) |
| Morocco Mirror | duplicate SKU |
| Sharkbait Polarized Bifocal | unreplaced IDs (7 Veeqo-absent; 9 pass through) |

---

## Monster

### validate_products — 277 → 268 passed, 9 flagged

| Product | Reasons |
|---|---|
| Locs Kong 9054 | no model |
| Socket Goggle | not in Veeqo + no model |
| Sunglass String Chum Strap | not in Veeqo + no model |
| proSPORT 30 PACK PM 2.5 Face Masks | no model |
| Ruby Extra Large Zipper Case | no model |
| Diamond Chrome Hard Case | no model |
| Sunglasses Repair Kit | no model |
| Sunglasses Repair Screw Driver | no model |
| Sunglasses Lens Cleaner | no model |

### validate_variations — 2,796 → 2,591 passed, 205 flagged

| Reason | Count |
|---|---|
| No NNXnn model | ~112 |
| Not in Veeqo | ~85 |
| Model mismatch: 25X65 vs 29X34 (Harvard) | 42 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 24 |
| Model mismatch: CA10X15CP vs CA10X16CP (Chipper) | 4 |
| Model mismatch: FLPL7X59SB vs FLPL73X31SB (Sharkbait Float) | 3 |

No-model flags cover: X-Loop (3322, 3304), Locs (Cruiser, Tuner, DeVille, Impala, Monte Carlo), VShield Face Shield, Bandannas, Face Masks, Mysto, Nautica, Ohana, Altitude Shield, Leopard Print Hard Case, Jade Deep Fabric Case, and others without NNXnn in their SKUs.

### create_items — 268 → 243 passed, 25 flagged

**No filled variations (variation gate cascaded):**
- Verbena Sun Reader (1 Veeqo-absent variation)
- Harvard Multifocal Reader (all model mismatch: 25X65 vs 29X34)
- Kumatage Bifocal (all model mismatch)
- Sharkbait Polarized Float (all model mismatch)
- Chipper Aviator (all model mismatch)
- Cooper Polarized Bifocal (4 Veeqo-absent)
- Mysto Sunglasses (all Veeqo-absent)
- Nautica Polarized (all Veeqo-absent)
- Ohana (all no model)
- Altitude Polarized Leather Shield (no model)
- Leopard Print Hard Case (no model)
- Jade Deep Fabric Case (no model)
- X-Loop 3322, X-Loop 3304 (no model)
- Locs Cruiser, Tuner, DeVille, Impala, Monte Carlo (no model)
- VShield Flip Up Face Shield (no model)
- VShield Vibrant Bandannas (no model)
- Black Reusable Stretch Face Mask (no model)
- Childrens Flip UP Shield (Veeqo-absent)

**Other:**
- Morocco Mirror — duplicate SKU
- Sharkbait Polarized Bifocal — unreplaced IDs (partial Veeqo absence; product survives with 9 passing variations)

---

## BikerShades

### validate_products — 704 → 541 passed, 163 flagged

BikerShades has a large tail of non-product WooCommerce listings. All 163 flagged products fail the no-NNXnn check; a subset also fail the Veeqo check.

**Categories of flagged products:**

| Category | Count (approx) |
|---|---|
| Rx service options (single vision, progressive, A/R, transitions, prism, etc.) | ~35 |
| Wiley X frames for Rx (per-model Rx frame listings) | ~25 |
| 7eye frames for Rx (per-model Rx frame listings) | ~18 |
| Ziena Rx frames | 6 |
| BikerArmour frames for Rx | ~4 |
| Try Before You Buy deposits (BikerArmour, WileyX, 7eye, combos) | ~8 |
| Accessories (cases, cleaning kits, repair kits, straps, foam seals) | ~10 |
| Service / operational (shipping labels, misc frame, custom product, invoice, warranty) | ~15 |
| Locs Kong 9054 (no NNXnn) | 1 |
| Other non-product (Return USPS label, misc shipping, space shield, medical goggle) | ~10 |
| Wiley X accessories (leash cord, t-peg strap, clamshell case, cleaning cloth) | 4 |

### validate_variations — 6,165 → 4,425 passed, 1,740 flagged

| Reason | Count |
|---|---|
| No NNXnn model | ~1,336 |
| Not in Veeqo | ~170 |
| Model mismatch: 25X65 vs 29X34 (Harvard) | 42 |
| Model mismatch: BF2X6KT vs BF4X7KT (Kumatage) | 26 |
| Model mismatch: other bifocal/reader conflicts | ~166 |

**No-model SKU patterns (the 1,336):**

- All 7eye base models (Aspen, Bali, Bora, Briza, Cape, Chubasco, Churada, Cyclone, Derby, Diablo, Raptor, Sedona, Sierra, Taku Plus, Ventus, Viento, Whirlwind) — 150+ variations
- All 7eye Eclipse XT photochromic models (same 15+ frames) — 300+ variations
- All Wiley X base models (Airrage, Boss, Brick, Enzo, Gravity, Sleek, Tide) — 20+ variations
- All Wiley X Eclipse XT models (12+ frames: Airrage, Boss, Brick, Censor, Enzo, Gravity, Hudson, Ignite, Kingpin, Nash, Omega, Ovation, Ozone, Grid, P17, Peak, Rebel, Romer3, Saint, Slay, Twisted, Valor, XL-1) — 250+ variations
- BikerArmour base models (Angel Rhinestones, Anaconda, Camber, Evolution, Magnum, Magnum Chrome, Socket, Vanguard, Tomahawk) — 100+ variations
- Locs (Cruiser, DeVille, Impala, Monte Carlo, Tuner) + X-Loop (3303, 3304, 3319, 3320, 3322) + Chopper 901 — 30+ variations
- Non-sunglasses (Face Masks, Bandannas, Face Shields) — 50+ variations
- Service/accessory items (Expedited Shipping, Warranty, Replacement Foam, Microfiber Cases) — 20+ variations

### create_items — 541 → 401 passed, 140 flagged

**7eye base models (17 flagged):**
7Eye Aspen, Bali, Bora, Briza, Cape, Chubasco, Churada, Cyclone, Derby, Diablo, Panhead, Raptor, Sedona, Sierra, Taku Plus, Ventus, Viento, Whirlwind — all variations have no NNXnn model, all removed.

**7eye Eclipse XT models (15 flagged):**
7eye Aspen, Bali, Bora, Briza, Cape, Chubasco, Churada, Derby, Diablo, Panhead, Raptor, Sedona, Sierra, Taku Plus, Ventus, Viento, Whirlwind, Warrior, Notus for Eclipse XT — all removed.

**Wiley X base models (7 flagged):**
Wiley X Airrage, Boss, Brick, Enzo, Gravity, Kingpin, Nash, Omega, P-17, Peak, Rebel, Rebel Alt Fit, Slay, Sleek, Tide, Twisted — all removed.

**Wiley X Eclipse XT models (12+ flagged):**
Wiley X Airrage, Boss, Brick, Censor, Enzo, Gravity, Hudson, Ignite, Kingpin, Nash, Omega, Ovation, Ozone, Grid, P17, Peak, Rebel, Rebel Alt Fit, Romer3, Saint, Slay, Sleek, Tide, Twisted, Valor, XL-1 for Eclipse XT — all removed.

**BikerArmour variants (5 flagged):**
BikerArmour Angel with Rhinestone [MED-LG], Socket Goggle [One Size], Vanguard [SM-MED], Camber [LG-XL], Tomahawk Eclipse Photochromic — all removed.

**Duplicate lens-type BikerArmour listings (7 flagged):**
Evolution Clear/HD/Yellow Lens (3 products), Anaconda Clear/HD/Yellow Lens (3 products), Socket Clear/HD/Yellow Lens (3 products), Angel Rhinestones Clear/Yellow Lens (2 products) — these are separate WC products per lens type that have no NNXnn in their variations.

**Locs / X-Loop / Chopper (9 flagged):**
Locs Cruiser, DeVille, Impala, Monte Carlo, Tuner; X-Loop 3304 Fender, 3322 Infield, 3319 Club, 3320 Sprint, 3303 Bogey; Chopper 901 — all removed.

**Bifocals/readers (6 flagged):**
Harvard Multifocal Reader (model mismatch 25X65 vs 29X34), Bypass Bifocal (Veeqo-absent + mismatch), Kumatage Bifocal (model mismatch), Finish Line Bifocal (Veeqo-absent), Starlet Bifocal (Veeqo-absent), Hawkeye HD Bifocal (partial Veeqo absence).

**Non-sunglasses (5 flagged):**
PM 2.5 Face Masks Pack of 3, 2 PACK Bandannas, VShield Flip Up Face Shield, Cabot Photochromic Reader (8/10 Veeqo-absent), Edison Photochromic Reader (8/10 Veeqo-absent).

**Service / accessory (9 flagged):**
1 Year NON Prescription Warranty, 7 Eye Replacement Foam, Expedited Shipping, Leopard Print Hard Case, Jade Deep Fabric Case, Blank Microfiber Cleaning Case, Biker Armour Microfiber Cleaning Case, Dynamo Combos [LG-XL], 7Eye Oasis [MED-LG].

**Other:**
Alpine Polarized Leather Shield, Altitude Polarized Leather Shield, Brooklyn, Aruba Polarized, Seaway (dup SKU + no filled), Sharkbait Polarized Float, Chipper, Camber Yellow Lens — all removed.

**Duplicate SKU flags:**
- Seaway — `CAPL14X64SW-0`
- Taxi Polarized Bifocal — `BFPL58X852TX-0`

---

## Cross-brand patterns

### Veeqo absence
Primarily affects high-power reader/bifocal variations (powers above +3.00) across all three brands — these SKUs exist in WooCommerce but were never stocked in Veeqo. Products with full Veeqo absence are dropped entirely; products with partial absence lose those variations but survive.

### Model number mismatch
Three recurring cross-brand cases:
- **Kumatage Bifocal** — BF2X6KT vs BF4X7KT (different frame models mixed into one WC product)
- **Sharkbait Polarized Float** — FLPL7X59SB vs FLPL73X31SB (same)
- **Chipper Aviator** — CA10X15CP vs CA10X16CP (same)
- **Harvard Multifocal Reader** — 25X65 vs 29X34 (multiple frame bases in one listing)

### BikerShades NNXnn gap
7eye, Wiley X, and BikerArmour frame SKUs do not follow the NNXnn model number convention used by proSPORT-originated frames. This causes 1,336 variation flags and cascades into 100+ product drops at create_items. These are real products but their SKU structure is opaque to the NNXnn check.

Two paths forward:
1. **Accept the loss** — BikerShades 401 items covers the BikerArmour original line, most polarized/bifocal products, readers, and Locs/X-Loop. 7eye and Wiley X are excluded.
2. **Extend the check** — add brand-keyed SKU pattern recognition for 7eye/WileyX/BikerArmour to validate_variations, allowing those frames through.

### Non-product WooCommerce tail (BikerShades only)
163 products flagged at validate_products are not sunglasses: Rx service add-ons, per-frame Rx listings, Try Before You Buy deposits, accessories, and operational entries. These require reimplementation as site features, not product migrations.

### Accessory products (all brands)
Cases, cleaning kits, repair kits, and similar accessories have no NNXnn SKU and are correctly filtered out across all three brands.

### Rx frame products slipping through (BikerShades)
Ten BikerShades Rx frame service listings made it into create-items because the `-RX` / `-HIGH-RX` suffix appears after the first hyphen segment, so `extract_model()` finds the valid NNXnn in the frame prefix and passes them:

| SKU | Name |
|---|---|
| `FM10X30CS-RX` | BikerArmour Camshaft for Rx |
| `GO47X11RB-RX` | Robin Goggle for Rx |
| `FM270X20TX-RX` | BikerArmour T-Rex for Rx |
| `FM5X1MR-RX` | BikerArmour Marauder for Rx |
| `FM85X11MNA-RX` | BikerArmour Angel for Rx |
| `FM11X81DM-BK-RX` | BikerArmour Dymo for High Rx |
| `FM540X548SH-BK-RX` | BikerArmour Shocker for High Rx |
| `FM5X14TR-BK-RX` | BikerArmour Trooper for Rx |
| `FM5X14TR-BK-HIGH-RX` | BikerArmour Trooper for High Power Rx |
| `FM0X76AB-HIGH-RX` | BikerArmour Air Boss for High Rx |

These are "send your frame for Rx glazing" service listings, not sellable products. They were previously caught by a `JUNK_SKU_CONTAINS` `-RX` hardcode in `create_items.py` that was removed. Fix: restore a BikerShades-keyed `-RX` suffix filter in `JUNK_SKU_CONTAINS` (or check any hyphen segment for the token, not just the first).
