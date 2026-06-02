# download-items verify — proSPORT Sunglasses

## Result

`verify_download_items.py` — 166 items, 411 URLs — **PASSED**

## Checks

| Check | Rule |
|---|---|
| Every URL accounted for | Every image URL from categorize-items is in `download_map` or `flagged` |
| Local files exist | Every `download_map` entry has a file on disk |
| No zero-byte files | All downloaded files have non-zero size |
| No product left imageless | No product has all its product images failed — would violate the "every product must have at least one image" constraint from `validate_products` |
