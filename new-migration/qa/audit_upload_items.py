import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "prosport": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir = BASE / "data" / slug

download_map = json.loads((data_dir / "download-items" / "download_map.json").read_text())
upload_map   = json.loads((data_dir / "upload-items"   / "upload_map.json").read_text())

local_paths    = set(download_map.values())
uploaded_paths = set(upload_map.keys())

not_uploaded      = local_paths - uploaded_paths
missing_from_disk = [p for p in uploaded_paths if not os.path.exists(p)]
bad_urls          = [u for u in upload_map.values() if not isinstance(u, str) or not u.startswith("https://")]
supabase_urls     = list(upload_map.values())
duplicate_urls    = len(supabase_urls) - len(set(supabase_urls))

print(f"audit_upload_items — {brand_name}")
print(f"  download_map entries : {len(download_map)}")
print(f"  unique local files   : {len(local_paths)}")
print(f"  uploaded             : {len(uploaded_paths)}")
print(f"  not yet uploaded     : {len(not_uploaded)}")
print(f"  bad Supabase URLs    : {len(bad_urls)}")
print(f"  duplicate URLs       : {duplicate_urls}")

if not_uploaded:
    print(f"\n── NOT UPLOADED ({len(not_uploaded)}) ──")
    for p in sorted(not_uploaded)[:10]:
        print(f"  {Path(p).name}")
    if len(not_uploaded) > 10:
        print(f"  ... and {len(not_uploaded) - 10} more")

if missing_from_disk:
    print(f"\n── IN UPLOAD_MAP BUT FILE GONE FROM DISK ({len(missing_from_disk)}) ──")
    for p in missing_from_disk[:10]:
        print(f"  {p}")

if bad_urls:
    print(f"\n── BAD SUPABASE URLs ({len(bad_urls)}) ──")
    for u in bad_urls[:5]:
        print(f"  {u}")
