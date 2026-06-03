import json
import time
import requests
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]
base_url = os.getenv(config["base_url"])
auth = (os.getenv(config["consumer_key"]), os.getenv(config["consumer_secret"]))

(BASE / "data" / slug).mkdir(parents=True, exist_ok=True)
out_dir = BASE / "data" / slug / "fetch-products"
out_dir.mkdir(exist_ok=True)

print(f"Brand: {brand_name} ({slug})")
print(f"Store: {base_url}")
print()

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

    products = r.json()
    if not products:
        print("No more products.")
        break

    all_products.extend(products)
    total = int(r.headers.get("X-WP-Total", 0))
    print(f"  {len(products)} products (total: {len(all_products)} / {total})")

    if len(all_products) >= total:
        break

    page += 1
    time.sleep(0.1)

out = out_dir / "products.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(all_products)} products → {out}")
print(f"\n  → Next: python pipeline/fetch_variations.py")
