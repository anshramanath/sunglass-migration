# Bikershades Migration — Claude Context

## What this is
Migrating product data from bikershades.com (WordPress/WooCommerce) into a new multi-brand Supabase-backed app. All scripts live in `migration/`.

## Pipeline (in order)
1. `fetch_products.py` — fetches 647 products from WooCommerce Store API
2. `fetch_variations.py` — fetches 6,064 variations (crash-safe, resumes)
3. `reshape_products.py` — normalizes data, buckets by issue type into `reshaped/`
4. `download_images.py` — downloads all images locally (crash-safe via `url_map.json`)
5. `upload_images.py` — uploads to Supabase Storage (crash-safe via `upload_map.json`)
6. `import_products.py` — inserts clean products into Supabase DB

## Key files
- `migration/db/001_initial_schema.sql` — source of truth for DB schema
- `migration/db/drop_schema.sql` — wipe all tables (dev only)
- `migration/images/clean-products/url_map.json` — bikershades URL → local path
- `migration/images/clean-products/upload_map.json` — local path → Supabase storage URL
- `reshaped-problems/` — triage notes for the 58 flagged products
- `PROGRESS.md` — full decision log
- `BACKEND_HANDOFF.md` — handoff doc for the Next.js admin/API/MCP app (moved by user)

## Image pipeline
Images are deduplicated by URL — `url_map.json` keys by full URL so the same image referenced across many products is only downloaded and uploaded once. Folder structure under `images/` is cosmetic; the map is the source of truth.

Image resolution chain in import: `bikershades URL → url_map → local path → upload_map → storage URL`. If either lookup fails the image is dropped (no broken URLs in DB).

## Database
- Supabase/Postgres, multi-brand schema
- `service_role` key used by backend — bypasses RLS
- Frontends never hit Supabase directly — go through Next.js backend
- `admins` table gates admin access (no public signup)
- Variation image stored inline on `variations` row (`image_src`, `image_name`) — variations have at most 1 image. More than 1 is a WooCommerce misconfiguration and gets bucketed separately.

## Reshaped buckets (current counts)
- `clean_products_shape.json` — 586 ✅
- `invalid_sku_products_shape.json` — 22
- `no_weight_products_shape.json` — 14 (includes weight=0.0)
- `zero_price_products_shape.json` — 8
- `missing_attributes_products_shape.json` — 7
- `duplicate_name_products_shape.json` — 6
- `no_image_products_shape.json` — 3
- `multiple_variation_images_products_shape.json` — 1

## Environment
`.env` at project root (gitignored). See `.env.example` for required variables. Scripts load it via `load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")`.

## Current state
Schema updated (variation_images table removed). Import needs to be re-run against the new schema. 58 flagged products pending owner review — see `reshaped-problems/treatment.md` for owner-facing questions.
