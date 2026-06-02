# Sunglass Monster Migration
Migrates brand product data from WooCommerce to Supabase.

---

## Brands

| Brand | Env Prefix | Store URL |
|-------|------------|-----------|
| proSPORT Sunglasses | `PROSPORT` | prosportsunglasses.com |

Set `BRAND="proSPORT Sunglasses"` in `.env` to select the active brand.

---

## Structure

```
new-migration/
  pipeline/      ← fetch, slim, validate, reshape, create, recategorize, download, upload, import
  analysis/      ← per-stage analysis scripts
  db/            ← schema SQL
  data/          ← per-brand output (data/{slug}/...)
  docs/          ← per-stage notes and analysis (docs/{stage}/)
```

---

## Running

```bash
# Set active brand in .env
BRAND="proSPORT Sunglasses"

# Products
python pipeline/fetch_products.py
python pipeline/slim_products.py
python pipeline/validate_products.py

# Variations
python pipeline/fetch_variations.py
python pipeline/slim_variations.py
python pipeline/validate_variations.py

# Reshape → create items
python pipeline/reshape_products.py
python pipeline/reshape_variations.py
python pipeline/create_items.py

# Recategorize → import
python pipeline/recategorize_items.py
python pipeline/download_images.py
python pipeline/upload_images.py
python pipeline/import_items.py
```

---

## Environment

`.env` at repo root. Required variables:

```env
DATABASE_URL=...
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...

BRAND="proSPORT Sunglasses"

PROSPORT_BASE_URL=https://prosportsunglasses.com
PROSPORT_CONSUMER_KEY=...
PROSPORT_CONSUMER_SECRET=...
```
