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

errors = []

# 1. Every local file on disk is in upload_map
unaccounted = [p for p in local_paths if p not in uploaded_paths and os.path.exists(p)]
if unaccounted:
    errors.append(f"{len(unaccounted)} local file(s) on disk missing from upload_map")

# 2. No extra paths in upload_map absent from download_map
extra = uploaded_paths - local_paths
if extra:
    errors.append(f"{len(extra)} path(s) in upload_map not in download_map")

# 3. All upload_map values are valid Supabase URLs
bad = [p for p, u in upload_map.items() if not isinstance(u, str) or not u.startswith("https://")]
if bad:
    errors.append(f"{len(bad)} upload_map value(s) are not valid URLs")

# 4. Every original URL resolves end-to-end: download_map url → local → upload_map → storage URL
broken_chain = [url for url, local in download_map.items() if local not in upload_map]
if broken_chain:
    errors.append(f"{len(broken_chain)} original URL(s) have no end-to-end resolution (will be dropped at import)")

print(f"verify_upload_items — {brand_name}")
print(f"  download_map : {len(download_map)} entries")
print(f"  upload_map   : {len(upload_map)} entries")
print(f"  full chain   : {len(download_map) - len(broken_chain)}/{len(download_map)} URLs resolvable\n")

if errors:
    print(f"  FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  [ERROR] {e}")
    if unaccounted:
        print()
        for p in unaccounted[:10]:
            print(f"    {Path(p).name}")
        if len(unaccounted) > 10:
            print(f"    ... and {len(unaccounted) - 10} more")
else:
    print(f"  PASSED — all checks clean")
