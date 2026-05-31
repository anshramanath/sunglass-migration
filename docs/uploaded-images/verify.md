# Uploaded Images Verify
_Last updated: 2026-05-30_

**Source:** `images/url_map.json` cross-referenced against `images/upload_map.json`

---

## Result

**All checks passed.** Every downloaded file has a corresponding Supabase URL. The full resolution chain (`bikershades URL → url_map → local path → upload_map → Supabase URL`) is intact for all 2,531 images.

---

## Checks

| Check | Result |
|-------|--------|
| Every local file is uploaded or gone from disk | ✅ 0 unaccounted |
| No extra paths in `upload_map` absent from `url_map` | ✅ 0 extra |
| All `upload_map` values are valid URLs | ✅ 0 blank or invalid |
| Every downloaded image resolves to a Supabase URL | ✅ 0 broken |

---

## Counts

| | Count |
|-|------:|
| Local files (`url_map`) | 2,531 |
| Uploaded (`upload_map`) | 2,531 |
| Full chain resolvable | 2,531 |
| Broken chain (would be dropped at import) | 0 |
