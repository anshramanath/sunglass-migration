import json
import os
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand
from veeqo import check_veeqo
from sku_structure import check_sku

brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
base_url   = config["base_url"]
auth       = (os.getenv(config["consumer_key"]), os.getenv(config["consumer_secret"]))

out_dir = BASE / "data" / slug / "fetch-products"
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Brand: {brand_name} ({slug})")
print(f"Store: {base_url}\n")

all_products = []
page = 1

while True:
    print(f"Fetching page {page}...")
    r = requests.get(
        f"{base_url}/wp-json/wc/v3/products",
        auth=auth,
        params={"per_page": 100, "page": page},
        timeout=30,
    )

    if r.status_code != 200:
        print(f"Stopped. HTTP {r.status_code}: {r.text[:300]}")
        break

    batch = r.json()
    if not batch:
        print("No more products.")
        break

    all_products.extend(batch)
    total = int(r.headers.get("X-WP-Total", 0))
    print(f"  {len(batch)} products ({len(all_products)} / {total})")

    if len(all_products) >= total:
        break

    page += 1
    time.sleep(0.1)

print("\nRunning checks...")

products  = []
flagged   = []
seen_skus = set()

for p in all_products:
    if p.get("type") != "simple":
        products.append(p)
        continue

    sku     = (p.get("sku") or "").strip()
    reasons = []

    if p.get("variations"):
        reasons.append("simple product has non-empty variations array")
    if not check_sku(sku):
        reasons.append("SKU does not match NNXnn structure")
    if not check_veeqo(sku):
        reasons.append("SKU not found in Veeqo")
    if sku in seen_skus:
        reasons.append(f"duplicate SKU: {sku!r}")
    else:
        seen_skus.add(sku)

    if reasons:
        flagged.append({"reasons": reasons, "product": p})
    else:
        products.append(p)

(out_dir / "products.json").write_text(json.dumps(products, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))

print(f"\nSaved {len(products)} products → {out_dir / 'products.json'}")
print(f"Saved {len(flagged)} flagged  → {out_dir / 'flagged.json'}")
