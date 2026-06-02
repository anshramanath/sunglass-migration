import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

BASE = Path(__file__).parent.parent  # new-migration/
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "proSPORT Sunglasses": {
        "slug": "prosport",
        "base_url": "PROSPORT_BASE_URL",
        "consumer_key": "PROSPORT_CONSUMER_KEY",
        "consumer_secret": "PROSPORT_CONSUMER_SECRET",
    },
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]
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
