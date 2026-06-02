import json
import os
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

with open(IMAGES_DIR / "upload_map.json") as f:
    upload_map = json.load(f)

errors = []
ok = []

def check(name, passed, detail=""):
    (ok if passed else errors).append(f"{name}{': ' + detail if detail else ''}")

local_paths = set(url_map.values())
uploaded_paths = set(upload_map.keys())

# ── 1. Every local file is either uploaded or missing from disk ───────────────

unaccounted = [p for p in local_paths if p not in uploaded_paths and os.path.exists(p)]
check("Every local file is uploaded or gone from disk", not unaccounted,
      f"{len(unaccounted)} files on disk but not in upload_map")

# ── 2. No path in upload_map that isn't in url_map ───────────────────────────

extra = uploaded_paths - local_paths
check("No extra paths in upload_map absent from url_map", not extra,
      f"{len(extra)} extra")

# ── 3. All Supabase URLs are non-empty strings ────────────────────────────────

bad = [p for p, u in upload_map.items() if not isinstance(u, str) or not u.strip()]
check("All upload_map values are valid URLs", not bad,
      f"{len(bad)} blank or invalid")

# ── 4. Every bikershades URL resolves end-to-end ─────────────────────────────

broken_chain = []
for bk_url, local in url_map.items():
    if local not in upload_map:
        broken_chain.append(bk_url)

check("Every downloaded image resolves to a Supabase URL",
      not broken_chain, f"{len(broken_chain)} broken (will be dropped at import)")

# ── Report ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("  UPLOADED IMAGES VERIFICATION")
print("=" * 60)
print(f"  Local files (url_map):    {len(local_paths)}")
print(f"  Uploaded (upload_map):    {len(uploaded_paths)}")
print(f"  Full chain resolvable:    {len(local_paths) - len(broken_chain)}")
print(f"  Broken chain (dropped):   {len(broken_chain)}")
print()

for name in ok:
    print(f"  ✓ {name}")
if errors:
    print()
    for e in errors:
        print(f"  ✗ {e}")
    if unaccounted:
        print()
        print("── FILES ON DISK NOT IN UPLOAD_MAP ──")
        for p in unaccounted[:10]:
            print(f"  {Path(p).name}")
        if len(unaccounted) > 10:
            print(f"  ... and {len(unaccounted) - 10} more")
else:
    print("  ALL CHECKS PASSED")

print()
print("  → Write a summary of these results in docs/uploaded-images/verify.md")
