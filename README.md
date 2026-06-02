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
  pipeline/      ← fetch, reshape, recategorize, download, upload, import
  qa/            ← audit + verify scripts for each step
  db/            ← schema SQL
  data/          ← per-brand output (data/{slug}/...)
  docs/          ← per-brand docs (docs/{slug}/...)
  CLAUDE.md      ← Claude Code context
  PROGRESS.md    ← decision log
  README.md      ← this file
```

---

## Running

```bash
# Set active brand in .env
BRAND="proSPORT Sunglasses"

# Run pipeline steps in order
python pipeline/fetch_products.py
python pipeline/fetch_variations.py
python pipeline/reshape_items.py
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
