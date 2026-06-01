# Uploaded Images Audit
_Last updated: 2026-05-31_

**Source:** `migration/images/upload_map.json` cross-referenced against `url_map.json`
**Local files:** 2,465 | **Uploaded:** 2,465

---

## Result

**All checks passed.** All 2,465 local files are uploaded to Supabase Storage. Zero gaps, zero bad URLs, zero duplicates.

---

## Counts

| Metric | Value |
|--------|------:|
| Local files (from url_map) | 2,465 |
| Uploaded (in upload_map) | 2,465 |
| Not yet uploaded | 0 |
| In upload_map but missing from disk | 0 |
| Bad Supabase URLs | 0 |
| Duplicate Supabase URLs | 0 |

---

## Notes

- Bucket: `bikershades` (public)
- Storage path = filename only (e.g. `2024_05_image.jpg`) — flat structure in bucket
- `upload_map.json` maps local path → Supabase public URL
- 2 files timed out on the first run; re-running resumed and uploaded them with zero failures.
