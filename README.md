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
| `migration/db/001_initial_schema.sql` | Source of truth for the Supabase database schema |
| `PROGRESS.md` | Full migration log — decisions, findings, field mappings |

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
[next] upload to storage + insert into Supabase
```

---

## 🚀 Running the scripts

**1. Install dependencies**
```bash
pip install requests
```

**2. Fetch all products**
```bash
cd migration
python fetch_products.py
```

**3. Fetch all variations**
```bash
python fetch_variations.py
```
✅ Crash-safe — resumes exactly where it left off if interrupted.

**4. Reshape into clean schema**
```bash
python reshape_products.py
```

**5. Download images**
```bash
python download_images.py
```
✅ Crash-safe — checkpoints after every image via `url_map.json`. Re-running skips already-downloaded files and retries failures.

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
| `clean_products_shape.json` | 589 | ✅ Ready for import |
| `invalid_sku_products_shape.json` | 22 | ⚠️ SKU is null or contains a space |
| `no_weight_products_shape.json` | 12 | ⚠️ Missing weight (needed for shipping) |
| `zero_price_products_shape.json` | 8 | ⚠️ Price is zero — internal/service products |
| `missing_attributes_products_shape.json` | 7 | ⚠️ Variations with no attribute data |
| `duplicate_name_products_shape.json` | 6 | ⚠️ Same name as another product |
| `no_image_products_shape.json` | 3 | ⚠️ No images at all |

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
  "attributes": ["blue-green-smoke", "glossy-black-green-smoke"],
  "variations": [
    {
      "attribute": ["blue-green-smoke"],
      "variation": { "sku": "SP47X96BS-BG", "regularPriceInCents": 1999, "..." }
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
| `variations` | Per-color/option variation data |
| `product_images` | Product gallery images |
| `variation_images` | Variation-specific images |
| `description_images` | Images embedded in description HTML |
| `admins` | Gates admin dashboard access via Supabase Auth |

---

## ✅ Progress

- [x] Fetch all products
- [x] Fetch all variations
- [x] Reshape into clean schema
- [x] Download images locally
- [x] Design database schema
- [ ] Upload images to storage
- [ ] Insert clean products into Supabase
- [ ] Manually review and fix flagged buckets
