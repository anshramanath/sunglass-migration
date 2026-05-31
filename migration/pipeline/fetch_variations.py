import json
import requests
from pathlib import Path

BASE = Path(__file__).parent.parent  # migration/
BASE_URL = "https://bikershades.com/wp-json/wc/store/products"
OUTPUT_FILE = BASE / "items/variations.json"
(BASE / "items").mkdir(parents=True, exist_ok=True)

with open(BASE / "items/products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

variable_products = [p for p in products if p.get("variations")]
print(f"Found {len(variable_products)} variable products.")

total_variations = sum(len(p["variations"]) for p in variable_products)
print(f"Total variations to fetch: {total_variations}")

# Load existing progress if resuming
try:
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)
    fetched_count = sum(len(v) for v in results.values())
    print(f"Resuming — {fetched_count} variations already fetched.\n")
except FileNotFoundError:
    results = {}
    fetched_count = 0

print(f"Remaining: {total_variations - fetched_count} variations\n")

for product in variable_products:
    parent_id = str(product["id"])

    all_variation_ids = [v["id"] for v in product["variations"]]

    # Find which variation IDs are already saved for this parent
    already_fetched_ids = {v["id"] for v in results.get(parent_id, [])}
    remaining_ids = [vid for vid in all_variation_ids if vid not in already_fetched_ids]

    if not remaining_ids:
        continue

    print(f"[{product['id']}] {product['name']} — {len(remaining_ids)} remaining of {len(all_variation_ids)}")

    for var_id in remaining_ids:
        try:
            response = requests.get(f"{BASE_URL}/{var_id}", timeout=30)

            if response.status_code != 200:
                print(f"  Failed {var_id}: HTTP {response.status_code}")
                continue

            variation = response.json()

            if parent_id not in results:
                results[parent_id] = []
            results[parent_id].append(variation)

            # Save after each individual variation
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            fetched_count += 1

        except Exception as e:
            print(f"  Error fetching {var_id}: {e}")

        # no sleep — network latency is the bottleneck

    print(f"  Done. ({fetched_count}/{total_variations} total fetched)\n")

print(f"Finished. {len(results)} parents saved to {OUTPUT_FILE}.")
