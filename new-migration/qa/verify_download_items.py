import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
data_dir  = BASE / "data" / slug
items_dir = data_dir / "download-items"

items        = json.loads((data_dir / "categorize-items" / "items.json").read_text())
download_map = json.loads((items_dir / "download_map.json").read_text())
flagged_data = json.loads((items_dir / "flagged.json").read_text()) if (items_dir / "flagged.json").exists() else {}

failed_urls  = {e["src"] for e in flagged_data.get("failed_to_download", [])}
accounted    = set(download_map.keys()) | failed_urls

errors = []

def err(msg):
    errors.append(msg)

# ── Every URL is accounted for ────────────────────────────────────────────────
for item in items:
    for img in item.get("images", []):
        src = img.get("src")
        if src and src not in accounted:
            err(f"id={item['id']} product image not in download_map or flagged: {src}")
    for url in item.get("descriptionImages", []):
        if url and url not in accounted:
            err(f"id={item['id']} description image not in download_map or flagged: {url}")
    for v in item.get("variations", []):
        if v.get("image") and v["image"].get("src"):
            src = v["image"]["src"]
            if src not in accounted:
                err(f"id={item['id']} variation {v['id']} image not in download_map or flagged: {src}")

# ── Every local path in download_map exists on disk ──────────────────────────
for url, local_path in download_map.items():
    if not Path(local_path).exists():
        err(f"download_map entry missing on disk: {local_path}")

# ── Every local file is non-zero bytes ───────────────────────────────────────
for url, local_path in download_map.items():
    p = Path(local_path)
    if p.exists() and p.stat().st_size == 0:
        err(f"zero-byte file: {local_path}")

# ── KEY CHECK: no product has all its images failed ───────────────────────────
# A product must have at least one successfully downloaded image (product images only —
# variation and description image failures are tolerated at the product level).
for item in items:
    product_srcs = [img["src"] for img in item.get("images", []) if img.get("src")]
    if not product_srcs:
        # Already caught at validate_products — skip here
        continue
    resolved = [src for src in product_srcs if src in download_map and Path(download_map[src]).exists()]
    if not resolved:
        err(
            f"id={item['id']} {item['name'][:45]!r} — all {len(product_srcs)} product image(s) failed to download; "
            f"product will be imageless at import"
        )

# ── Report ────────────────────────────────────────────────────────────────────
print(f"verify_download_items — {brand_name}")
print(f"  items        : {len(items)}")
print(f"  download_map : {len(download_map)} entries")
print(f"  failed       : {len(failed_urls)} URLs\n")

if errors:
    print(f"FAILED — {len(errors)} error(s):")
    for e in errors:
        print(f"  [ERROR] {e}")
else:
    print("PASSED — all checks clean")
