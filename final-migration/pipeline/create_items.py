import json
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand
from veeqo import check_veeqo
from sku_structure import get_structure

brand_key, config = load_brand()
slug     = config["slug"]
brand_name = config["brand_name"]
base_url = config["base_url"]
auth     = (os.getenv(config["consumer_key"]), os.getenv(config["consumer_secret"]))

in_path = BASE / "data" / slug / "fetch-products" / "products.json"
if not in_path.exists():
    raise SystemExit(f"Run fetch_products.py first. Not found: {in_path}")

products = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "create-items"
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Brand: {brand_name} ({slug})")
print(f"{len(products)} products\n")

items   = []
flagged = []

for p in products:
    pid            = p["id"]
    variation_ids  = p.get("variations", [])

    if not variation_ids:
        items.append({**p, "variations": []})
        continue

    print(f"Fetching variations for '{p['name']}' (id={pid})...")

    fetched     = []
    flag_reasons = []
    page        = 1

    while True:
        r = requests.get(
            f"{base_url}/wp-json/wc/v3/products/{pid}/variations",
            auth=auth,
            params={"per_page": 100, "page": page},
            timeout=30,
        )
        if r.status_code != 200:
            flag_reasons.append(f"API error fetching variations: HTTP {r.status_code}")
            break

        batch = r.json()
        if not batch:
            break

        for v in batch:
            if v.get("parent_id") != pid:
                flag_reasons.append(f"variation {v['id']} has parent_id={v.get('parent_id')}, expected {pid}")
            else:
                fetched.append(v)

        if len(batch) < 100:
            break

        page += 1
        time.sleep(0.1)

    print(f"  {len(fetched)} variations fetched")

    if flag_reasons:
        flagged.append({"reasons": flag_reasons, "product": p})
    else:
        items.append({**p, "variations": fetched})

print("\nRunning checks...")

clean = []
for item in items:
    reasons    = []
    variations = item.get("variations", [])

    if not variations:
        clean.append(item)
        continue

    # drop non-objects and variations not in Veeqo
    valid = [v for v in variations if isinstance(v, dict) and check_veeqo((v.get("sku") or "").strip())]

    if len(valid) < 2:
        reasons.append(f"fewer than 2 valid variations ({len(valid)} remaining)")
    else:
        seen_skus  = set()
        structures = set()
        for v in valid:
            sku = (v.get("sku") or "").strip()

            if sku in seen_skus:
                reasons.append(f"variation {v['id']} has duplicate SKU {sku!r}")
            else:
                seen_skus.add(sku)

            s = get_structure(sku)
            if s:
                structures.add(s)

        if len(structures) > 1:
            reasons.append(f"mixed SKU structures across variations: {sorted(structures)}")

    if reasons:
        flagged.append({"reasons": reasons, "product": item})
    else:
        clean.append({**item, "variations": valid})

(out_dir / "items.json").write_text(json.dumps(clean, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

print(f"\nSaved {len(clean)} items   → {out_dir / 'items.json'}")
print(f"Saved {len(flagged)} flagged → {out_dir / 'flagged.json'}")
