import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "generate-content" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run generate_content.py (and MCP server) first. Not found: {in_path}")

items = json.loads(in_path.read_text())

# Strip "includes case" bullets
case_stripped = 0
for item in items:
    before = len(item.get("summary") or [])
    item["summary"] = [
        b for b in (item.get("summary") or [])
        if not (b.lower().startswith("includes") and "case" in b.lower())
    ]
    case_stripped += before - len(item["summary"])

# Deduplicate by slug — keep first occurrence
seen_slugs = set()
deduped = []
dropped_names = []
for item in items:
    s = item["slug"]
    if s in seen_slugs:
        dropped_names.append(item["name"])
    else:
        seen_slugs.add(s)
        deduped.append(item)

out_dir = BASE / "data" / slug / "clean-content"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "items.json").write_text(json.dumps(deduped, indent=2, ensure_ascii=False))

print(f"Input:  {len(items)} items")
print(f"Output: {len(deduped)} items")
print(f"  Case bullets stripped: {case_stripped}")
print(f"  Duplicates dropped:    {len(dropped_names)}")
if dropped_names:
    for name in dropped_names:
        print(f"    - {name}")
