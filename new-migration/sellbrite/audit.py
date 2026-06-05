"""
Audit Sellbrite variation groups against Veeqo.

Pipeline per group:
  1. Veeqo     — all child_skus present in Veeqo CSV
                 (groups with non-standard/manually-typed SKUs fail here naturally)
  2. Mismatch  — check if child_skus share the same base (segment before first '-')
                 C-prefix rule: CPR... and PR... count as the same base

Output → sellbrite/data/
  flagged.json   — groups with a base SKU mismatch
  clean.json     — groups that passed all checks
  skipped.json   — groups that failed the Veeqo check (with reason)
"""

import csv
import json
import re
from pathlib import Path

from dotenv import load_dotenv

HERE = Path(__file__).parent
ROOT = HERE.parent
load_dotenv(dotenv_path=ROOT.parent / ".env")

groups_path = HERE / "data" / "variation_groups.json"
if not groups_path.exists():
    raise SystemExit("Run fetch.py first.")

csv_candidates = sorted((ROOT.parent).glob("sellables_export*.csv"))
if not csv_candidates:
    raise SystemExit(f"No sellables_export*.csv found in {ROOT.parent}")
csv_path = csv_candidates[0]

# ── load ───────────────────────────────────────────────────────────────────────

groups = json.loads(groups_path.read_text())

veeqo_skus = set()
with open(csv_path, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        sku = row.get("sku_code", "").strip()
        if sku:
            veeqo_skus.add(sku)

print(f"Variation groups:  {len(groups):,}")
print(f"Veeqo SKUs:        {len(veeqo_skus):,}")
print()


# ── helpers ────────────────────────────────────────────────────────────────────

def normalize_base(base: str) -> str:
    # C-prefix rule: CPR... and PR... are the same family
    return re.sub(r"^C(?=[A-Z])", "", base)


def base_sku(sku: str) -> str:
    return normalize_base(sku.split("-")[0])


# ── audit ──────────────────────────────────────────────────────────────────────

clean   = []
flagged = []
skipped = []

for g in groups:
    child_skus = [s.strip() for s in (g.get("child_skus") or []) if s.strip()]
    group_sku  = g.get("sku", "")

    if not child_skus:
        skipped.append({"reason": "no child_skus", "group": g})
        continue

    # 1. veeqo presence
    absent = [s for s in child_skus if s not in veeqo_skus]
    if absent:
        skipped.append({
            "reason": f"{len(absent)}/{len(child_skus)} child SKUs absent from Veeqo",
            "absent_skus": absent,
            "group": g,
        })
        continue

    # 3. base mismatch
    bases = {base_sku(s) for s in child_skus}
    if len(bases) > 1:
        flagged.append({
            "bases": sorted(bases),
            "child_skus": child_skus,
            "group": g,
        })
    else:
        clean.append(g)


# ── output ─────────────────────────────────────────────────────────────────────

out_dir = HERE / "data"
(out_dir / "clean.json").write_text(json.dumps(clean, indent=2, ensure_ascii=False))
(out_dir / "flagged.json").write_text(json.dumps(flagged, indent=2, ensure_ascii=False))
(out_dir / "skipped.json").write_text(json.dumps(skipped, indent=2, ensure_ascii=False))

# skipped breakdown
skip_veeqo = sum(1 for s in skipped if "Veeqo" in s["reason"])
skip_empty = sum(1 for s in skipped if "no child" in s["reason"])

print(f"Results:")
print(f"  Clean (passed all checks):  {len(clean):,}")
print(f"  Flagged (base mismatch):    {len(flagged):,}")
print(f"  Skipped — no child SKUs:    {skip_empty:,}")
print(f"  Skipped — absent from Veeqo:{skip_veeqo:,}")
print()

if flagged:
    print("Flagged groups:")
    for f in flagged:
        name = f["group"].get("sku", "")[:50]
        print(f"  {name}")
        print(f"    bases: {f['bases']}")
        print(f"    SKUs:  {f['child_skus'][:3]}{'...' if len(f['child_skus']) > 3 else ''}")
    print()

print(f"Saved → {out_dir}/clean.json ({len(clean)} groups)")
print(f"Saved → {out_dir}/flagged.json ({len(flagged)} groups)")
print(f"Saved → {out_dir}/skipped.json ({len(skipped)} groups)")
