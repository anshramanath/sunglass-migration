import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "dedup-images" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run dedup_images.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "generate-content"
out_dir.mkdir(parents=True, exist_ok=True)

output = []
for item in items:
    output.append({
        **item,
        "wasMissingDescription": item.get("description") is None,
        "wasMissingSummary":     not item.get("summary"),
    })

missing_desc = sum(1 for i in output if i["wasMissingDescription"])
missing_sum  = sum(1 for i in output if i["wasMissingSummary"])

(out_dir / "items.json").write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Initialized {len(output)} items → {out_dir / 'items.json'}")
print(f"  wasMissingDescription: {missing_desc}")
print(f"  wasMissingSummary:     {missing_sum}")
