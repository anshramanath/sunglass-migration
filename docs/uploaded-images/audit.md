# Uploaded Images Audit
_Last updated: 2026-05-30_

**Source:** `images/url_map.json` → `images/upload_map.json`
**Local files:** 2,531 | **Supabase bucket:** `bikershades`

---

## Result

**Zero issues.** All 2,531 local files uploaded successfully. Full resolution chain intact end-to-end.

---

## Summary

| Metric | Count |
|--------|------:|
| Local files (from `url_map.json`) | 2,531 |
| Uploaded (in `upload_map.json`) | 2,531 |
| Not yet uploaded | 0 |
| In map but missing from disk | 0 |
| Bad Supabase URLs | 0 |
| Duplicate Supabase URLs | 0 |

---

## Notes

- 1 file failed on first run with a 503 (server blip) — retried successfully on second run.
- All local paths in `url_map.json` map to a valid Supabase public URL in `upload_map.json`.
