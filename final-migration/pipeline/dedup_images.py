import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "merge-attributes" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run merge_attributes.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "dedup-images"
out_dir.mkdir(parents=True, exist_ok=True)

product_dups    = 0
variation_dups  = 0

output = []
for item in items:
    # dedup productImages by src, preserve order
    seen = set()
    clean_product_imgs = []
    for img in item.get("productImages", []):
        if img["src"] not in seen:
            seen.add(img["src"])
            clean_product_imgs.append(img)
        else:
            product_dups += 1

    product_srcs = {img["src"] for img in clean_product_imgs}

    # dedup variationImages against product srcs
    updated_variations = []
    for v in item.get("variations", []):
        clean_var_imgs = []
        for img in v.get("variationImages", []):
            if img["src"] in product_srcs:
                variation_dups += 1
            else:
                clean_var_imgs.append(img)
        updated_variations.append({**v, "variationImages": clean_var_imgs})

    output.append({
        **item,
        "productImages": clean_product_imgs,
        "variations":    updated_variations,
    })

(out_dir / "items.json").write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Product image duplicates removed:   {product_dups}")
print(f"Variation image duplicates removed: {variation_dups}")
print(f"Saved {len(output)} items → {out_dir / 'items.json'}")
