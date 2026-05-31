# Uploaded Images Verify
_Last updated: 2026-05-31_

**Source:** Full chain `bikershades URL → url_map → local path → upload_map → Supabase URL` for all 2,531 files

---

## Result

**All checks passed.** Every downloaded image resolves end-to-end to a Supabase URL. Zero broken chains.

---

## Checks

| Check | Result |
|-------|--------|
| Every local file is in upload_map | ✅ |
| No extra paths in upload_map absent from url_map | ✅ |
| All upload_map values are valid Supabase URLs | ✅ |
| Every downloaded image resolves to a Supabase URL | ✅ |

---

## Counts

| Metric | Value |
|--------|------:|
| Local files (url_map) | 2,531 |
| Uploaded (upload_map) | 2,531 |
| Full chain resolvable | 2,531 |
| Broken chain (dropped at import) | 0 |
