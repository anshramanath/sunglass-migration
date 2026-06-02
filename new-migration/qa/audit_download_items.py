import json
import os
from collections import Counter
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
data_dir  = BASE / "data" / slug
items_dir = data_dir / "download-items"

items       = json.loads((data_dir / "categorize-items" / "items.json").read_text())
download_map = json.loads((items_dir / "download_map.json").read_text())
flagged_data = json.loads((items_dir / "flagged.json").read_text()) if (items_dir / "flagged.json").exists() else {}

failed_urls = {e["src"] for e in flagged_data.get("failed_to_download", [])}
collisions  = flagged_data.get("collisions", [])

SEP  = "=" * 60
DASH = "─" * 60

print(SEP)
print(f"  DOWNLOAD ITEMS AUDIT — {brand_name}")
print(SEP)

# ── Coverage ──────────────────────────────────────────────────────────────────
print(f"\n── URL coverage ──")
print(f"  download_map entries : {len(download_map)}")
print(f"  failed to download   : {len(failed_urls)}")
print(f"  collisions           : {len(collisions)}")

# ── Local file integrity ──────────────────────────────────────────────────────
print(f"\n── Local file integrity ──")
missing_files  = [p for p in download_map.values() if not Path(p).exists()]
present_files  = [p for p in download_map.values() if Path(p).exists()]
print(f"  files present on disk : {len(present_files)}")
print(f"  files missing on disk : {len(missing_files)}")
if missing_files:
    for p in missing_files[:5]:
        print(f"    {p}")

# file size stats
if present_files:
    sizes = [Path(p).stat().st_size for p in present_files]
    sizes_kb = [s / 1024 for s in sizes]
    print(f"  size range : {min(sizes_kb):.1f} KB – {max(sizes_kb):.1f} KB")
    print(f"  total size : {sum(sizes) / 1024 / 1024:.1f} MB")
    zero_byte = sum(1 for s in sizes if s == 0)
    if zero_byte:
        print(f"  zero-byte files : {zero_byte}")

# ── By image type ─────────────────────────────────────────────────────────────
print(f"\n── URLs by image type ──")
product_urls     = {img["src"] for p in items for img in p.get("images", []) if img.get("src")}
variation_urls   = {img["src"] for p in items for v in p.get("variations", []) for img in v.get("images", []) if img.get("src")}
description_urls = {img["src"] for p in items for img in p.get("descriptionImages", []) if isinstance(img, dict) and img.get("src")}

for label, url_set in [("product_image", product_urls), ("variation_image", variation_urls), ("description_image", description_urls)]:
    downloaded = len(url_set & set(download_map))
    failed     = len(url_set & failed_urls)
    print(f"  {label:<20} total={len(url_set)}  downloaded={downloaded}  failed={failed}")

# ── File extension distribution ───────────────────────────────────────────────
print(f"\n── File extensions ──")
ext_counter = Counter(Path(p).suffix.lower() for p in download_map.values())
for ext, count in ext_counter.most_common():
    print(f"  {ext or '(none)':<10} {count}")

# ── Collisions ────────────────────────────────────────────────────────────────
if collisions:
    print(f"\n── Filename collisions ({len(collisions)}) ──")
    for c in collisions[:10]:
        print(f"  existing: {c['existing']['src']}")
        print(f"  tried   : {c['tried']['src']}")
        print()
