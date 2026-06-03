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

products_path = BASE / "data" / slug / "validate-products" / "products.json"
if not products_path.exists():
    raise SystemExit(f"Run validate_products.py first. Not found: {products_path}")

out_dir = BASE / "data" / slug / "fetch-variations"
out_dir.mkdir(parents=True, exist_ok=True)

out_path = out_dir / "variations.json"

products = json.loads(products_path.read_text())
variable = [p for p in products if p.get("variations")]

print(f"Brand: {brand_name} ({slug})")
print(f"Store: {base_url}")
print(f"Variable products: {len(variable)}")
print()

# Load progress — stored as list of {product_id: int, variations: [...]}
# Keep an in-memory dict for fast lookup during the run
entries = []
fetched = {}  # pid -> index in entries
if out_path.exists():
    entries = json.loads(out_path.read_text())
    fetched = {e["product_id"]: i for i, e in enumerate(entries)}
    print(f"Resuming — {len(fetched)}/{len(variable)} products already fetched\n")

for i, product in enumerate(variable):
    pid = product["id"]
    expected = len(product["variations"])

    if pid in fetched:
        print(f"[{i+1}/{len(variable)}] id={pid} — skipped (already fetched {len(entries[fetched[pid]]['variations'])} variations)")
        continue

    print(f"[{i+1}/{len(variable)}] id={pid} ({product['name'][:50]}) — {expected} variations...")

    variations = []
    page = 1

    while True:
        r = requests.get(
            f"{base_url}/wp-json/wc/v3/products/{pid}/variations",
            auth=auth,
            params={"per_page": 100, "page": page},
            timeout=30,
        )

        if r.status_code != 200:
            print(f"  ERROR HTTP {r.status_code}: {r.text[:200]}")
            break

        batch = r.json()
        if not batch:
            break

        for v in batch:
            returned_parent = v.get("parent_id")
            if returned_parent != pid:
                print(f"  MISMATCH: variation id={v.get('id')} returned parent_id={returned_parent}, expected {pid}")
            variations.append(v)

        total = int(r.headers.get("X-WP-Total", 0))
        if len(variations) >= total:
            break

        page += 1
        time.sleep(0.1)

    if len(variations) != expected:
        print(f"  WARNING: expected {expected}, got {len(variations)}")
    else:
        print(f"  OK ({len(variations)} variations)")

    entry = {"product_id": pid, "variations": variations}
    fetched[pid] = len(entries)
    entries.append(entry)
    out_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False))

    time.sleep(0.1)

total = sum(len(e["variations"]) for e in entries)
print(f"\nTotal variations: {total}")
print(f"Saved → {out_path}")
print(f"\n  → Next: python pipeline/slim_variations.py")
