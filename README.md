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

Brands are configured in `final-migration/config/__init__.py`. Set the active brand at runtime:

```bash
BRAND=prosport python final-migration/pipeline/fetch_products.py
```

## Setup

- Python dependencies: `requests`, `python-dotenv`, `mcp`
- `.env` at repo root with WooCommerce credentials per brand and `VEEQO_KEY`
- Veeqo CSV export (`sellables_export*.csv`) placed in `final-migration/pipeline/`
- Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json` — points to `final-migration/mcp/server.py`

## Pipeline

See `PIPELINE.md` for the full step-by-step pipeline.
