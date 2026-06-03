# reshape-products notes — Sunglass Monster

## Run

269 products reshaped. No errors.

## Attribute name cleaning

Generic rules (all brands):
- Strip `for Filter` postfix
- Strip `Choose ` prefix
- Strip `Filter by ` prefix
- Strip parentheticals e.g. `(REQUIRED)`

Monster overrides (brand-specific):
- `Cleaner Spray Bottle QTY` → `Quantity`
- `Qty` → `Quantity`
- `Frame Styles for Filter` → `Style`
- `Special Size for Filter` → `Size`

Final attribute names: `Activity`, `Brand`, `Color`, `Foam Type`, `Frame Color`, `Gender`, `Lens Color`, `Lens Type`, `Material`, `Power`, `Size`, `Style`

## Fix made during this run

`verify_reshape_products.py` had a stale inline `clean_attr_name` missing the `Filter by` prefix strip, parenthetical strip, and brand overrides. Updated to match reshape script logic.
