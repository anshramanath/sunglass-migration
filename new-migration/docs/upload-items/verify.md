# upload-items verify — proSPORT Sunglasses

## Result

`verify_upload_items.py` — 411 entries, 411/411 chains resolvable — **PASSED**

## Checks

| Check | Rule |
|---|---|
| Every local file is uploaded | Every path in `download_map` values is a key in `upload_map` (or no longer on disk) |
| No extra paths in upload_map | No `upload_map` key that isn't in `download_map` values |
| All URLs are valid | Every `upload_map` value is a non-empty `https://` string |
| Full chain resolvable | Every original URL in `download_map` has a corresponding `upload_map` entry |
