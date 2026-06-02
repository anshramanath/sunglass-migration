# download-items notes — proSPORT Sunglasses

## Results

- Input: `categorize-items/items.json` (166 items)
- Output: `download-items/local/` (411 files), `download-items/download_map.json`, `download-items/flagged.json`
- Script: `pipeline/download_items.py`

## What this step does

Downloads all unique image URLs referenced in `categorize-items/items.json` to a local folder. Three image sources are collected: product gallery images, variation images (non-null only), and description images. URLs are deduplicated — the same URL appearing across multiple products is downloaded once.

## Crash safety

`download_map.json` is written after every successful download. On resume, any URL already in the map is skipped. `flagged.json` is updated after every attempt, logging all failed URLs and filename collisions.

## Filename convention

Everything after `/uploads/` in the URL path, with `/` replaced by `_`:

```
https://prosportsunglasses.com/wp-content/uploads/2020/11/Cabriolet-Gloss-Black-Front.jpg
→ images/2020_11_Cabriolet-Gloss-Black-Front.jpg
```

The year/month prefix from WordPress's folder structure is baked into the filename, eliminating collisions between files with the same basename uploaded in different months.

## Output structure

```
data/prosport/download-items/
  download_map.json   { original URL → absolute local path }
  flagged.json        { failed_to_download: [...], collisions: [...] }
  images/             all downloaded image files (flat)
    2020_11_Cabriolet-Gloss-Black-Front.jpg
    ...
```

## Map chain

```
original URL → download_map → local path → upload_map → Supabase URL
```

`download_map` is the first link. At import time, both maps must resolve for an image to be written to the DB.

## Design decisions

- **Failed downloads are not blockers** — a 404 means the image no longer exists on the origin server. The pipeline continues and logs the failure. At import time, unresolvable images are silently dropped.
- **Exception**: a product whose every product image fails to download is flagged by `verify_download_items.py` — this violates the "every product must have at least one image" constraint established at `validate_products`.
