# bikershades-migration

WooCommerce → Supabase migration pipeline for a multi-brand sunglass platform.

## Active work

All current migration work lives in `final-migration/`. The `old-migration/` and `new-migration/` directories are abandoned and kept only for reference.

## Structure

```
final-migration/
  config/         Brand configuration and .env loading
  pipeline/       Scripts run in sequence per brand
  mcp/            MCP server for AI content generation via Claude Desktop
  db/             Supabase schema
  docs/           Analysis docs and remove/merge plans
  data/           Output data (gitignored)
```

## Brands

| Brand key | DB slug | Display name |
|---|---|---|
| `prosport` | `prosport-sunglasses` | proSPORT Sunglasses |
| `monster` | `sunglass-monster` | Sunglass Monster |
| `bikershades` | `bikershades` | BikerShades |

Set the active brand at runtime:

```bash
BRAND=prosport python final-migration/pipeline/fetch_products.py
```

## Setup

- Python dependencies: `requests`, `python-dotenv`, `mcp`, `supabase`, `psycopg2`
- `.env` at repo root with:
  - WooCommerce credentials per brand (`WC_URL`, `WC_KEY`, `WC_SECRET`)
  - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
  - `DATABASE_URL` (use Supabase session pooler URL — direct connection uses IPv6 and may fail on some networks)
- Veeqo CSV export (`sellables_export*.csv`) placed in `final-migration/pipeline/`
- Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json` — points to `final-migration/mcp/server.py`

## Pipeline

See `PIPELINE.md` for the full step-by-step pipeline. The pipeline runs per brand through step 16 (upload), then import can be run for all brands independently.

Current status: all three brands fully imported into Supabase. Pipeline complete.

| Brand | Products | Notes |
|---|---|---|
| prosport-sunglasses | 150 | 0 images skipped |
| sunglass-monster | 256 | 1 image skipped (confirmed 404) |
| bikershades | 464 | 78 images skipped (confirmed 404s) |
