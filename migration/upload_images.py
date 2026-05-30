import json
import os
import mimetypes
import time
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
BUCKET = "product-images"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

try:
    supabase.storage.create_bucket(BUCKET, options={"public": True})
    print(f"Created bucket: {BUCKET}")
except Exception:
    print(f"Bucket: {BUCKET} (already exists)")

IMAGES_DIR = Path("images/clean-products")
URL_MAP_PATH = IMAGES_DIR / "url_map.json"
UPLOAD_MAP_PATH = IMAGES_DIR / "upload_map.json"

with open(URL_MAP_PATH) as f:
    url_map = json.load(f)

if UPLOAD_MAP_PATH.exists():
    with open(UPLOAD_MAP_PATH) as f:
        upload_map = json.load(f)
else:
    upload_map = {}

# Unique local paths — dedup is automatic since url_map maps many URLs to one local file
unique_paths = list(set(url_map.values()))
total = len(unique_paths)

uploaded = 0
already_done = 0
skipped_missing = 0
failed = 0

print(f"\n{total} unique local files to process...\n")

for local_path in unique_paths:
    if not os.path.exists(local_path):
        skipped_missing += 1
        continue

    if local_path in upload_map:
        already_done += 1
        continue

    # Strip "images/" prefix for the storage path
    storage_path = local_path[len("images/"):]

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

        with open(UPLOAD_MAP_PATH, "w") as f:
            json.dump(upload_map, f)

        uploaded += 1
        if uploaded % 100 == 0:
            print(f"  {uploaded} uploaded...")

    except Exception as e:
        print(f"  FAIL {local_path}: {e}")
        failed += 1

    time.sleep(0.02)

print(f"\nDone.")
print(f"  {uploaded} uploaded")
print(f"  {already_done} already done (resume)")
print(f"  {skipped_missing} skipped (no local file — 404'd during download)")
print(f"  {failed} failed")
print(f"  Upload map saved → {UPLOAD_MAP_PATH}")
