"""
Fetch all Sellbrite variation groups.
Each group has: sku (family identifier), child_skus (real WC SKUs),
description, images[], and variation_attributes.

Credentials in .env:
  SELLBRITE_ACCESS_TOKEN
  SELLBRITE_SECRET_KEY
  SELLBRITE_BASE_URL   (default: https://api.sellbrite.com/v1)

Output → new-migration/sellbrite/data/variation_groups.json
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).parent
ROOT = HERE.parent
load_dotenv(dotenv_path=ROOT.parent / ".env")

ACCESS_TOKEN = os.getenv("SELLBRITE_ACCESS_TOKEN", "")
SECRET_KEY   = os.getenv("SELLBRITE_SECRET_KEY", "")
BASE_URL     = os.getenv("SELLBRITE_BASE_URL", "https://api.sellbrite.com/v1").rstrip("/")

if not ACCESS_TOKEN or not SECRET_KEY:
    raise SystemExit("Missing SELLBRITE_ACCESS_TOKEN or SELLBRITE_SECRET_KEY in .env")

AUTH  = (ACCESS_TOKEN, SECRET_KEY)
LIMIT = 100
DELAY = 0.15

out_dir = HERE / "data"
out_dir.mkdir(exist_ok=True)


def fetch_all(path: str) -> list:
    results = []
    page = 1
    while True:
        print(f"  page {page}...", end="\r")
        r = requests.get(
            f"{BASE_URL}{path}",
            auth=AUTH,
            params={"limit": LIMIT, "page": page},
            timeout=30,
        )
        if r.status_code != 200:
            raise SystemExit(f"HTTP {r.status_code} — {path}\n{r.text[:400]}")
        data = r.json()
        if not isinstance(data, list) or not data:
            break
        results.extend(data)
        if len(data) < LIMIT:
            break
        page += 1
        time.sleep(DELAY)
    return results


print("Fetching variation_groups...")
groups = fetch_all("/variation_groups")

out_path = out_dir / "variation_groups.json"
out_path.write_text(json.dumps(groups, indent=2, ensure_ascii=False))

total_children  = sum(len(g.get("child_skus") or []) for g in groups)
has_description = sum(1 for g in groups if (g.get("description") or "").strip())
has_images      = sum(1 for g in groups if g.get("images"))

print(f"  {len(groups):,} groups             ")
print()
print(f"  Total child SKUs:    {total_children:,}")
print(f"  Has description:     {has_description:,} / {len(groups):,}  ({has_description/len(groups)*100:.0f}%)")
print(f"  Has images:          {has_images:,} / {len(groups):,}  ({has_images/len(groups)*100:.0f}%)")
print()
print(f"Saved → {out_path}")
