# 🕶️ Bikershades Migration
_Last updated: 2026-05-30_

Migrating product data from bikershades.com (WordPress/WooCommerce) into a clean, normalized schema for a new multi-brand app backed by Supabase.

---

## 📦 What's in here

**Pipeline** (`migration/pipeline/`)
| File | Description |
|---|---|
| `fetch_products.py` | Fetches all 647 products from the WooCommerce API |
| `fetch_variations.py` | Fetches all 6,064 product variations |
| `reshape_items.py` | Cleans and normalizes raw data, buckets by issue type |
| `recategorize_items.py` | Applies drops, merges, collapses to category links; outputs `recategorized/` |
| `download_images.py` | Downloads all product, variation, and description images locally |
| `upload_images.py` | Uploads local images to Supabase Storage, outputs `upload_map.json` |
| `import_items.py` | Inserts clean products into Supabase DB |

**QA** (`migration/qa/`)
| File | Description |
|---|---|
| `audit_shaped_items.py` | Validates all fields in shaped items for existence and correct values |
| `verify_shaped_items.py` | Cross-references reshaped output against raw — all 647 accounted for, no data loss |
| `audit_categorized_items.py` | Validates category path structure — leaf-only assignments, valid levels/slugs, tree stats |
| `verify_categorized_items.py` | Cross-references all three recategorized outputs — 586 total accounted for, no dropped/merged slugs |
| `audit_downloaded_images.py` | Checks url_map coverage, file integrity, failed/collision counts, coverage by image type |
| `verify_downloaded_images.py` | Cross-references all image URLs in items against url_map and failed.json — no URLs lost |
| `audit_uploaded_images.py` | Checks upload_map coverage, URL validity, missing files |
| `verify_uploaded_images.py` | Verifies every downloaded file resolves to a Supabase URL end-to-end |
| `audit_import.py` | Checks DB row counts, brands, category tree depth, duplicate SKUs, products with no images |
| `verify_import.py` | Cross-references DB against source — SKUs, field values, variation counts, category leaf slugs |

**Schema** (`migration/db/`)
| File | Description |
|---|---|
| `001_initial_schema.sql` | Source of truth for the Supabase database schema |
| `drop_schema.sql` | Wipes all tables for clean schema re-apply (dev only) |

**Docs** (`docs/`)
| File | Description |
|---|---|
| `completed.md` | Full pipeline audit for current run — filled in after each step |
| `completed_1.md` | Previous run results (pre price/stock schema changes) |
| `migration_seed.md` | Original migration guide |
| `shaped-items/` | Field-level audit, verify, attribute analysis, category link counts |
| `categorized-items/` | Categorized items audit and verify results |
| `downloaded-images/` | Download audit and verify results |
| `uploaded-images/` | Upload audit and verify results |
| `imported-items/` | Import audit and verify results |

**Root**
| File | Description |
|---|---|
| `PROGRESS.md` | Full migration log — decisions, findings, field mappings |
| `CLAUDE.md` | Claude Code context file — auto-loaded each session |
| `.env.example` | Template showing required environment variables |
| `migration/requirements.txt` | Python dependencies |
| `reshaped-problems/` | Manual review notes for flagged reshaped buckets |

---

## 🔄 Migration Pipeline

```
WooCommerce Store API
        ↓
fetch_products.py         → items/products.json (647 products)
        ↓
fetch_variations.py       → items/variations.json (6,064 variations)
        ↓
reshape_items.py          → reshaped/ — shaped_items.json (586) + 7 problem buckets
        ↓
recategorize_items.py     → recategorized/ — categorized_items.json (581) + no_category_items.json (2) + single_leaf_items.json (3)
        ↓
download_images.py        → images downloaded locally
        ↓
upload_images.py          → images uploaded to Supabase Storage
        ↓
import_items.py           → inserts categorized items into Supabase DB
```

---

## 🚀 Running the scripts

**1. Install dependencies**
```bash
pip install -r migration/requirements.txt
```

**2. Set up `.env`** in the project root (see `.env.example`):
```env
DATABASE_URL=postgresql://postgres:<password>@db.<project>.supabase.co:5432/postgres
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_SERVICE_KEY=<service_role key>
```

**3. Run the schema** in Supabase SQL editor:
```
migration/db/001_initial_schema.sql
```

**4. Fetch all products**
```bash
python migration/pipeline/fetch_products.py
```

**5. Fetch all variations**
```bash
python migration/pipeline/fetch_variations.py
```
✅ Crash-safe — resumes exactly where it left off if interrupted.

**6. Reshape into clean schema**
```bash
python migration/pipeline/reshape_items.py
```

**7. Recategorize**
```bash
python migration/pipeline/recategorize_items.py
```
Applies drops and merges, removes single-item leaves, strips non-leaf paths. Result: 8 trees, max depth 2 from root to leaf, products only at leaves. Outputs three buckets to `recategorized/`.

**8. Download images**
```bash
python migration/pipeline/download_images.py
```
✅ Crash-safe — checkpoints after every image via `url_map.json`. Images named using the path after `/uploads/` or `/gallery/` with `/` replaced by `_` (e.g. `2024_05_image.jpg`) — globally unique, no collisions. Failed downloads tracked in `failed.json` with `{sku, src}`.

**9. Upload images to Supabase Storage**
```bash
python migration/pipeline/upload_images.py
```
✅ Crash-safe — checkpoints after every upload via `upload_map.json`. Creates a `bikershades` bucket automatically (per-brand bucket model).

**10. Import into DB**
```bash
python migration/pipeline/import_items.py
```
⚠️ Wipes all existing product data first (`TRUNCATE brands CASCADE`), then inserts fresh.

---

## 📊 Catalog Stats

| | Count |
|---|---|
| Total products | 647 |
| Variable products | 486 |
| Simple products | 161 |
| Total variations | 6,064 |
| Shaped items (post-reshape) | 564 |
| Categorized items (post-recategorize) | 581 |
| Flagged for review | 83 |

---

## 🗂️ Output Buckets

### `reshaped/` — output of `reshape_items.py`
| File | Count | Reason |
|---|---|---|
| `shaped_items.json` | 564 | ✅ Passes to recategorize |
| `invalid_sku_items.json` | 22 | ⚠️ SKU is null or contains a space |
| `mismatched_attr_items.json` | 22 | ⚠️ Variation slugs not in product attribute terms |
| `no_weight_items.json` | 14 | ⚠️ Missing or zero weight |
| `zero_price_items.json` | 10 | ⚠️ Price is zero (product or all variations) |
| `duplicate_name_items.json` | 6 | ⚠️ Same name as another item |
| `missing_attributes_items.json` | 5 | ⚠️ Variations with completely empty attribute list |
| `no_image_items.json` | 3 | ⚠️ No images at all |
| `multiple_variation_images_items.json` | 1 | ⚠️ Variation has more than 1 image |

### `recategorized/` — output of `recategorize_items.py`
| File | Count | Reason |
|---|---|---|
| `categorized_items.json` | 581 | ✅ Ready for import — all paths end at leaf nodes |
| `no_category_items.json` | 2 | ⚠️ All category links were dropped — owner review needed |
| `single_leaf_items.json` | 3 | ⚠️ Only item in their leaf category — owner review needed |

---

## 📝 Manual Review Notes

Detailed review sheets for flagged buckets now live in `reshaped-problems/`.

Current files:
- `reshaped-problems/diagnosis.md` — high-level overview of all buckets and blockers
- `reshaped-problems/treatment.md` — owner-facing action doc with questions + live site links
- `reshaped-problems/zero_price_review.md`
- `reshaped-problems/no_weight_review.md`
- `reshaped-problems/no_image_review.md`
- `reshaped-problems/invalid_sku_review.md`
- `reshaped-problems/missing_attributes_review.md`
- `reshaped-problems/duplicate_name_review.md`

Current direction:
- All 6 buckets triaged with per-product notes
- `diagnosis.md` — high-level summary of every bucket and what's blocking it
- `treatment.md` — owner-facing action doc with every question + live site links
- Next step: share `treatment.md` with the owner to unblock the remaining 57 products

---

## 🧼 Clean Product Shape

```json
{
  "name": "Backspin Sport Sunglasses",
  "slug": "backspin-sport-sunglasses",
  "sku": "SP47X96BS-0",
  "wpUrl": "https://bikershades.com/shop/...",
  "productUrl": "https://bikershades.com/wp-json/wc/store/products/67767",
  "description": "Capture the essence of athletic performance...",
  "descriptionImgs": ["https://bikershades.com/wp-content/uploads/diagram.jpg"],
  "summary": ["Fits Large to X-Large heads", "Impact resistant lenses"],
  "sale": true,
  "minPriceCents": 1999,
  "maxPriceCents": 3499,
  "salePriceCents": null,
  "stock": 1,
  "categories": [
    [
      {"level": 1, "name": "Sunglasses", "slug": "sunglasses"},
      {"level": 2, "name": "Brands", "slug": "brands"},
      {"level": 3, "name": "ProSport", "slug": "prosport"}
    ]
  ],
  "images": [{ "src": "https://...", "name": "Backspin Front" }],
  "attributes": [
    {
      "name": "color",
      "terms": [
        { "name": "Blue Green Smoke", "slug": "blue-green-smoke" },
        { "name": "Glossy Black Green Smoke", "slug": "glossy-black-green-smoke" }
      ]
    }
  ],
  "variations": [
    {
      "attribute": ["blue-green-smoke"],
      "variation": { "sku": "SP47X96BS-BG", "regularPriceCents": 1999, "salePriceCents": 1599 }
    }
  ],
  "weight": 2,
  "weightUnit": "oz",
  "dimensions": { "length": 6, "width": 3, "height": 3 },
  "dimensionUnit": "in"
}
```

---

## 🗄️ Database Schema

Multi-brand Supabase/Postgres. See `migration/db/001_initial_schema.sql`.

| Table | Purpose |
|---|---|
| `brands` | One row per brand — `name` + `slug` (matches Storage bucket name) |
| `categories` | Nav categories, scoped per brand — self-referential `parent_id` forms a tree the owner can edit, create, and restructure through the admin |
| `products` | Core product catalog |
| `product_categories` | Many-to-many junction |
| `variations` | Per-color/option variation data — `attribute text[]` stores the selection combo |
| `product_images` | Product gallery images |
| `variation_images` | Variation-specific images (unique shots not already in product gallery) |
| `description_images` | Images embedded in description HTML |
| `admins` | Gates admin dashboard access via Supabase Auth |

---

## ✅ Progress

- [x] Fetch all products (647)
- [x] Fetch all variations (6,064)
- [x] Reshape into clean schema — 564 clean, 83 flagged across 8 buckets
- [x] Recategorize — 581 ready, 2 no-category, 3 single-leaf
- [x] Design database schema (price range, stock int, no ratings, variation_images table)
- [x] Download images — 2,531 downloaded, 30 permanent 404s
- [x] Upload images to Supabase Storage — 2,531 uploaded, 0 broken
- [x] Drop and re-apply schema in Supabase
- [x] Import into Supabase DB — 581 products, 5,649 variations, all QA passed
- [ ] Manually review and fix flagged buckets (66 total)
