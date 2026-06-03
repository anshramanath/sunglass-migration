# upload-items notes — proSPORT Sunglasses

## Results

- Input: `download-items/download_map.json` (411 entries)
- Output: `upload-items/upload_map.json` (411 entries)
- Script: `pipeline/upload_items.py`
- Bucket: `prosport` (Supabase Storage, public)

## What this step does

Uploads every unique local image file from `download-items/images/` to Supabase Storage. Reads `download_map.json` to get the set of unique local paths, deduplicates, and uploads each file. Writes the result to `upload_map.json` mapping `local path → Supabase public URL`.

## Crash safety

`upload_map.json` is written after every successful upload. On resume, any local path already in the map is skipped. Duplicate errors from Supabase (file already exists in the bucket) are handled gracefully — the public URL is fetched and the entry is added to the map.

## Storage path

Each file is stored at the bucket root using just its filename:

```
local: .../download-items/images/2020_11_Cabriolet-Gloss-Black-Front.jpg
→ bucket: prosport/2020_11_Cabriolet-Gloss-Black-Front.jpg
```

## Output structure

```
data/prosport/upload-items/
  upload_map.json   { absolute local path → Supabase public URL }
```

## Map chain

```
original URL → download_map → local path → upload_map → Supabase URL
```

`upload_map` is the second and final link. At import time, both maps must resolve for an image to be written to the DB.

## Design decisions

- **Bucket name = slug** — `prosport` bucket isolates this brand's assets. Adding a second brand means a new bucket, no cross-contamination.
- **Flat bucket structure** — images stored at the root of the bucket with no subdirectories, matching the flat `images/` folder from download.
- **Duplicate handling** — if a file already exists in the bucket (e.g. from a previous partial run), the upload catches the duplicate error, fetches the existing public URL, and records it. No manual cleanup needed between runs.
