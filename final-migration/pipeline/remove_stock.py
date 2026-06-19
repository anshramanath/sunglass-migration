import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "decode-entities" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run decode_entities.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

for item in items:
    item.pop("stock",   None)
    item.pop("inStock", None)
    for v in (item.get("variations") or []):
        v.pop("stock", None)

out_dir = BASE / "data" / slug / "remove-stock"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False))
print(f"Done. {len(items)} items written.")
