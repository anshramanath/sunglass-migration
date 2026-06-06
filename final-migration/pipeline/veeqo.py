import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import VEEQO_KEY

def check_veeqo(sku: str) -> bool:
    if not VEEQO_KEY:
        raise SystemExit("VEEQO_KEY not set in .env")

    r = requests.get(
        "https://api.veeqo.com/products",
        headers={"x-api-key": VEEQO_KEY},
        params={"query": sku},
        timeout=30,
    )
    if r.status_code != 200:
        raise SystemExit(f"Veeqo API error {r.status_code}: {r.text[:300]}")

    for product in r.json():
        for sellable in product.get("sellables", []):
            if sellable.get("sku_code", "").strip() == sku:
                return True

    return False
