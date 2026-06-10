import json
import mimetypes
import os
import sys
import time
from pathlib import Path

from supabase import create_client

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug       = config["slug"]
brand_slug = config["brand_slug"]
brand_name = config["brand_name"]

SUPABASE_URL         = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
BUCKET               = brand_slug

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

try:
    supabase.storage.create_bucket(BUCKET, options={"public": True})
    print(f"Created bucket: {BUCKET}")
except Exception:
    print(f"Bucket: {BUCKET} (already exists)")

map_path = BASE / "data" / slug / "download-items" / "download_map.json"
if not map_path.exists():
    raise SystemExit(f"Run download_items.py first. Not found: {map_path}")

out_dir = BASE / "data" / slug / "upload-items"
out_dir.mkdir(parents=True, exist_ok=True)
upload_map_path = out_dir / "upload_map.json"

download_map = json.loads(map_path.read_text())
upload_map   = json.loads(upload_map_path.read_text()) if upload_map_path.exists() else {}

unique_paths = list(set(download_map.values()))
print(f"Uploading {len(unique_paths)} unique files → bucket '{BUCKET}'")

uploaded = skipped = failed = 0

for local_path in unique_paths:
    if not os.path.exists(local_path):
        print(f"  MISSING: {local_path}")
        continue

    if local_path in upload_map:
        skipped += 1
        continue

    storage_path = Path(local_path).name
    content_type, _ = mimetypes.guess_type(local_path)
    if not content_type:
        content_type = "image/jpeg"

    try:
        with open(local_path, "rb") as f:
            supabase.storage.from_(BUCKET).upload(
                path=storage_path,
                file=f.read(),
                file_options={"content-type": content_type},
            )
        public_url = supabase.storage.from_(BUCKET).get_public_url(storage_path)
        upload_map[local_path] = public_url
        upload_map_path.write_text(json.dumps(upload_map, indent=2, ensure_ascii=False))
        uploaded += 1
        if uploaded % 50 == 0:
            print(f"  {uploaded} uploaded...")
    except Exception as e:
        if "Duplicate" in str(e):
            public_url = supabase.storage.from_(BUCKET).get_public_url(storage_path)
            upload_map[local_path] = public_url
            upload_map_path.write_text(json.dumps(upload_map, indent=2, ensure_ascii=False))
            uploaded += 1
        else:
            print(f"  FAIL {local_path}: {e}")
            failed += 1

    time.sleep(0.02)

print(f"Done. {uploaded} uploaded, {skipped} skipped (resume), {failed} failed")
print(f"upload_map → {upload_map_path}  ({len(upload_map)} entries)")
