# validate-products notes — Sunglass Monster

## Run

277 → 269 passed, 8 flagged (9 issues).

## Fix made during this run

`validate_products.py` had a `slugify(name) == slug` check that compared a programmatically generated slug against WooCommerce's stored slug. Worked coincidentally for ProSport's simple category names, but Monster's slugs diverge significantly from their names (e.g., `"Men's Glasses"` → stored as `"men-glasses"` not `"mens-glasses"`; `"Men Polarized Bifocals & Readers"` → stored as `"polarized-bifocals-readers"`). WooCommerce slugs are set at category creation and never auto-update — they're the ground truth. Removed the comparison; now only checks name and slug are non-empty strings.
