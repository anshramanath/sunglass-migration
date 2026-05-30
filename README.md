# 🕶️ Bikershades Migration

Migrating product data from bikershades.com (WordPress/WooCommerce) into a clean, normalized schema for a new multi-brand app backed by Supabase.

---

## 📦 What's in here

| File | Description |
|---|---|
| `migration/fetch_products.py` | Fetches all 647 products from the WooCommerce API |
| `migration/fetch_variations.py` | Fetches all 6,064 product variations |
| `migration/reshape_products.py` | Cleans and normalizes raw data, buckets by issue type |
| `migration/download_images.py` | Downloads all product, variation, and description images locally |
| `migration/upload_images.py` | Uploads local images to Supabase Storage, outputs `upload_map.json` |
| `migration/import_products.py` | Inserts clean products into Supabase DB |
| `migration/db/001_initial_schema.sql` | Source of truth for the Supabase database schema |
| `PROGRESS.md` | Full migration log — decisions, findings, field mappings |
| `reshaped-problems/` | Manual review notes for flagged reshaped buckets |

---

## 🔄 Migration Pipeline

```
WooCommerce Store API
        ↓
fetch_products.py       → products.json (647 products)
        ↓
fetch_variations.py     → variations.json (6,064 variations)
        ↓
reshape_products.py     → 7 bucketed JSON files in reshaped/
        ↓
download_images.py      → 2,785 images downloaded locally
        ↓
upload_images.py        → images uploaded to Supabase Storage, upload_map.json written
        ↓
import_products.py      → 589 clean products inserted into Supabase DB
```

---

## 🚀 Running the scripts

**1. Install dependencies**
```bash
pip install requests supabase psycopg2-binary python-dotenv
```

**2. Set up `.env`** in the project root:
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
cd migration
python fetch_products.py
```

**5. Fetch all variations**
```bash
python fetch_variations.py
```
✅ Crash-safe — resumes exactly where it left off if interrupted.

**6. Reshape into clean schema**
```bash
python reshape_products.py
```

**7. Download images**
```bash
python download_images.py
```
✅ Crash-safe — checkpoints after every image via `url_map.json`.

**8. Upload images to Supabase Storage**
```bash
python upload_images.py
```
✅ Crash-safe — checkpoints after every upload via `upload_map.json`. Creates `product-images` bucket automatically.

**9. Import products into DB**
```bash
python import_products.py
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
| Clean products | 589 |
| Flagged for review | 58 |
| Images downloaded | 2,785 |

---

## 🗂️ Reshaped Output Buckets

| File | Count | Reason |
|---|---|---|
| `clean_products_shape.json` | 588 | ✅ Ready for import |
| `invalid_sku_products_shape.json` | 22 | ⚠️ SKU is null or contains a space |
| `no_weight_products_shape.json` | 14 | ⚠️ Missing or zero weight (needed for shipping) |
| `zero_price_products_shape.json` | 8 | ⚠️ Price is zero — internal/service products |
| `missing_attributes_products_shape.json` | 7 | ⚠️ Variations with no attribute data |
| `duplicate_name_products_shape.json` | 6 | ⚠️ Same name as another product |
| `no_image_products_shape.json` | 3 | ⚠️ No images at all |
| `multiple_variation_images_products_shape.json` | 1 | ⚠️ Variation has more than 1 image — likely WooCommerce misconfiguration |

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
    { "name": "prosport-sunglasses", "link": "https://bikershades.com/product-category/..." }
  ],
  "images": [{ "src": "https://...", "name": "Backspin Front" }],
  "attributes": [
    { "name": "color", "terms": ["blue-green-smoke", "glossy-black-green-smoke"] }
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
| `brands` | One row per brand |
| `categories` | Nav/filter categories, scoped per brand |
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
- [ ] Manually review and fix flagged buckets
