import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "reshape-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run reshape_items_1.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "reshape-items-2"
out_dir.mkdir(parents=True, exist_ok=True)

reshaped = []
for item in items:
    reshaped.append(item)

(out_dir / "items.json").write_text(json.dumps(reshaped, indent=2, ensure_ascii=False))
print(f"Saved {len(reshaped)} items → {out_dir / 'items.json'}")
