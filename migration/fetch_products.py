import json
import time
import requests

BASE_URL = "https://bikershades.com/wp-json/wc/store/products"
PER_PAGE = 100

all_products = []
page = 1

while True:
    url = f"{BASE_URL}?per_page={PER_PAGE}&page={page}"

    print(f"Fetching page {page}...")
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"Stopped. HTTP {response.status_code}")
        print(response.text[:500])
        break

    products = response.json()

    if not isinstance(products, list):
        print("Stopped. Response was not a list.")
        print(products)
        break

    if len(products) == 0:
        print("No more products.")
        break

    all_products.extend(products)
    print(f"Fetched {len(products)} products from page {page}.")

    page += 1
    time.sleep(0.5)

with open("products.json", "w", encoding="utf-8") as file:
    json.dump(all_products, file, indent=2, ensure_ascii=False)

print(f"Saved {len(all_products)} total products to products.json")
