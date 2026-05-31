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
| `verify_shaped_items.py` | Cross-references reshaped output against raw + checks no field was dropped |
| `audit_categorized_items.py` | Validates category path structure in categorized items; reports tree stats per root |
| `verify_categorized_items.py` | Cross-references categorized against shaped — no items lost, counts match, no dropped/merged slugs survived |

**Schema** (`migration/db/`)
| File | Description |
|---|---|
| `001_initial_schema.sql` | Source of truth for the Supabase database schema |
| `drop_schema.sql` | Wipes all tables for clean schema re-apply (dev only) |

**Docs** (`docs/`)
| File | Description |
|---|---|
| `AUDIT_REPORT.md` | Full field-level audit results for clean products |
| `bikershades_migration_guide.md` | Original migration guide |

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
fetch_variations.py       → items/variations/variations.json (6,064 variations)
        ↓
reshape_items.py          → reshaped/ — shaped_items.json (586) + 7 problem buckets
        ↓
recategorize_items.py     → recategorized/ — categorized_items.json (584) + no_category_items.json (2)
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
Applies drops, merges, collapses. Outputs `recategorized/categorized_items.json` (clean) and `recategorized/no_category_items.json` (flagged for owner review).

**8. Download images**
```bash
python migration/pipeline/download_images.py
```
✅ Crash-safe — checkpoints after every image via `url_map.json`. Downloads clean products only into `migration/images/local/` (flat folder, deduplicated filenames).

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
| Variable products | 489 |
| Simple products | 157 |
| Total variations | 6,064 |
| Shaped items (post-reshape) | 586 |
| Categorized items (post-recategorize) | 584 |
| Flagged for review | 63 |

---

## 🗂️ Output Buckets

### `reshaped/` — output of `reshape_items.py`
| File | Count | Reason |
|---|---|---|
| `shaped_items.json` | 586 | ✅ Passes to recategorize |
| `invalid_sku_items.json` | 22 | ⚠️ SKU is null or contains a space |
| `no_weight_items.json` | 14 | ⚠️ Missing or zero weight |
| `zero_price_items.json` | 8 | ⚠️ Price is zero |
| `missing_attributes_items.json` | 7 | ⚠️ Variations with no attribute data |
| `duplicate_name_items.json` | 6 | ⚠️ Same name as another item |
| `no_image_items.json` | 3 | ⚠️ No images at all |
| `multiple_variation_images_items.json` | 1 | ⚠️ Variation has more than 1 image |

### `recategorized/` — output of `recategorize_items.py`
| File | Count | Reason |
|---|---|---|
| `categorized_items.json` | 584 | ✅ Ready for import |
| `no_category_items.json` | 2 | ⚠️ All category links were dropped — owner review needed |

---

## 📝 Manual Review Notes

Detailed review sheets for flagged buckets now live in `reshaped-problems/`.

Current files:
- `reshaped-problems/diagnosis.md` — high-level overview
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
  "regularPriceInCents": 2599,
  "salePriceInCents": 1999,
  "averageRating": 4.5,
  "reviewCount": 12,
  "inStock": true,
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
      "variation": { "sku": "SP47X96BS-BG", "regularPriceInCents": 1999 }
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
| `variations` | Per-color/option variation data — includes `image_src` and `image_name` directly on the row (variations have at most 1 image) |
| `product_images` | Product gallery images |
| `description_images` | Images embedded in description HTML |
| `admins` | Gates admin dashboard access via Supabase Auth |

---

## ✅ Progress

- [x] Fetch all products
- [x] Fetch all variations
- [x] Reshape into clean schema
- [x] Download images locally
- [x] Design database schema
- [x] Upload images to Supabase Storage
- [x] Insert clean products into Supabase
- [x] Audit and verify reshape accuracy
- [x] Schema update — variation image flattened onto variations row, variation_images table removed
- [ ] Re-run import against updated schema
- [ ] Manually review and fix flagged buckets

### Pending before import
- **Import script** — needs to populate `brands.slug`, `categories.slug`, and `categories.parent_id`; must key category dedup/lookup on `slug` not `name` (display names not unique — "See All" appears under multiple parent paths)
