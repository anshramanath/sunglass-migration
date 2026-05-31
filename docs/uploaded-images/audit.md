# Uploaded Images Audit
_Last updated: 2026-05-31_

**Source:** `migration/images/upload_map.json` cross-referenced against `url_map.json`
**Local files:** 2,531 | **Uploaded:** 2,531

---

## Result

**All checks passed.** All 2,531 local files are uploaded to Supabase Storage. Zero gaps, zero bad URLs, zero duplicates.

---

## Counts

| Metric | Value |
|--------|------:|
| Local files (from url_map) | 2,531 |
| Uploaded (in upload_map) | 2,531 |
| Not yet uploaded | 0 |
| In upload_map but missing from disk | 0 |
| Bad Supabase URLs | 0 |
| Duplicate Supabase URLs | 0 |

---

## Notes

- Bucket: `bikershades` (public)
- Storage path = filename only (e.g. `2024_05_image.jpg`) — flat structure in bucket
- `upload_map.json` maps local path → Supabase public URL
- One file was uploaded during the first run but not written to the map before the process was killed. The upload script was patched to handle 409 Duplicate responses gracefully (fetches public URL instead of failing), and the file was recovered on the next run.
