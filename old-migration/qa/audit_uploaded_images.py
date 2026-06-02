import json
import os
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
IMAGES_DIR = BASE / "images"

with open(IMAGES_DIR / "url_map.json") as f:
    url_map = json.load(f)

with open(IMAGES_DIR / "upload_map.json") as f:
    upload_map = json.load(f)

local_paths = set(url_map.values())
uploaded_paths = set(upload_map.keys())

total_local = len(local_paths)
total_uploaded = len(uploaded_paths)
not_uploaded = local_paths - uploaded_paths
missing_from_disk = [p for p in uploaded_paths if not os.path.exists(p)]

# Check Supabase URL format
supabase_urls = list(upload_map.values())
bad_urls = [u for u in supabase_urls if not u.startswith("https://")]
duplicate_urls = len(supabase_urls) - len(set(supabase_urls))

print("=" * 60)
print("  UPLOADED IMAGES AUDIT")
print("=" * 60)
print(f"  Local files (from url_map):    {total_local}")
print(f"  Uploaded (in upload_map):      {total_uploaded}")
print(f"  Not yet uploaded:              {len(not_uploaded)}")
print(f"  In upload_map but missing disk:{len(missing_from_disk)}")
print(f"  Bad Supabase URLs:             {len(bad_urls)}")
print(f"  Duplicate Supabase URLs:       {duplicate_urls}")

if not_uploaded:
    print()
    print("── NOT UPLOADED ──")
    for p in sorted(not_uploaded)[:10]:
        print(f"  {Path(p).name}")
    if len(not_uploaded) > 10:
        print(f"  ... and {len(not_uploaded) - 10} more")

if missing_from_disk:
    print()
    print("── IN UPLOAD_MAP BUT FILE GONE FROM DISK ──")
    for p in missing_from_disk[:10]:
        print(f"  {p}")

if bad_urls:
    print()
    print("── BAD SUPABASE URLs ──")
    for u in bad_urls[:5]:
        print(f"  {u}")

print()
print("  → Write a summary of these results in docs/uploaded-images/audit.md")
