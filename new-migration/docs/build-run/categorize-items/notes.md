# categorize-items notes — proSPORT Sunglasses

## Results

- Input: `create-items/items.json` (166 items)
- Output: `categorize-items/items.json` (166 items)
- Script: `pipeline/prosport_categorize_items.py`

## What this step does

Replaces the raw WooCommerce `categories[]` field on every item with a structured array of path arrays — each path being an ordered `[{level, name, slug}]` list from root to leaf. Only leaf categories carry products; parents are structural.

## Passes

**Pass 1 — HTML decode + normalize**
All category names are HTML-decoded (`&amp;` → `&`) then mapped through `RENAME_MAP` to their new title-case names. Dropped categories (`Uncategorized`, `Big and Tall`) are discarded. Parent slugs from WooCommerce (e.g. `readers-special-fit`) are filtered out — only leaf slugs are kept.

**Pass 2 — Hardcoded assignments**
21 products that had only `Uncategorized` in WooCommerce are assigned a leaf slug by id. 9 sunglasses receive a style or reader leaf; 12 cases and accessories receive `accessories`.

**Pass 3 — Build path arrays**
For each leaf slug, the tree definition (`TREE`) is used to look up its parent. A path array of `{level, name, slug}` objects is constructed — level 1 parent then level 2 child for nested leaves, or a single level 1 entry for root-level leaves (`accessories`). All paths for a product are wrapped in an outer array.

## Naming convention

- Title case: every word capitalised except `and`
- Slug: `name.lower().replace(' ', '-')`
- Round-trip: `slugify(name) == slug` and `namify(slug) == name`
- `&` not allowed in names — replaced with `and`

## Tree definition

```
Shop By Style → Sport, Street, Metal and Aviators
Lens Color    → Polarized, Hd Copper, Clear and Yellow
Readers Special Fit → Bifocals, Full Lens
Accessories   → (root-level leaf, no parent)
```

## Design decisions

- **Brand-specific script** — `prosport_categorize_items.py` contains the `RENAME_MAP`, `TREE`, and `HARDCODED` assignments for ProSport. Each brand gets its own script since category structure and uncategorized assignments are subjective per brand.
- **Only leaves carry products** — parent categories are structural only. Verified by checks in both the pipeline script and `verify_categorize_items.py`.
- **Array of path arrays** — `categories` is `[[{level, name, slug}, ...], ...]` so each parent-child pair is unambiguously linked. A flat list would break the parent→child relationship for multi-leaf products.
- **New Arrivals collapsed** — Big and Tall, Small and Petit, Asian Fit dropped. The 2 BIG & TALL products already had real categories (Sport, Street) so collapsing cost 0 homeless products.
- **Accessories is a new category** — not present in WooCommerce. Created to give the 12 cases and accessories products a proper home rather than leaving them uncategorized.

## Flagged / known issues

None — all 166 items categorized cleanly, all checks passed.
