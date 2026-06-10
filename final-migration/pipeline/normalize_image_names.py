import json
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "categorize-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run the categorize script first. Not found: {in_path}")

items = json.loads(in_path.read_text())


def normalize_name(src):
    stem = Path(urlparse(src).path).stem
    return stem.replace("-", " ").replace("_", " ")


def normalize_images(imgs):
    for img in imgs:
        img["name"] = normalize_name(img["src"])
    return imgs


for item in items:
    normalize_images(item.get("productImages") or [])
    normalize_images(item.get("descriptionImages") or [])
    for v in item.get("variations") or []:
        normalize_images(v.get("variationImages") or [])

out_dir = BASE / "data" / slug / "normalize-images"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False))

print(f"Normalized image names for {len(items)} items → {out_dir / 'items.json'}")
