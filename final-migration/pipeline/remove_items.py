import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "validate-items" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_items.py first. Not found: {in_path}")

REMOVE = {
    "bikershades": {
        "simple": {
            "FM10X30CS-RX", "7EYE-KAI-RX", "WX-CENSOR-RX", "FM0X76AB-HIGH-RX",
            "FM270X20TX-RX", "FM5X1MR-RX", "FM11X81DM-BK-RX", "FM540X548SH-BK-RX",
            "FM5X14TR-BK-RX", "FM5X14TR-BK-HIGH-RX", "FM85X11MNA-RX", "GO84X75BL-RX",
            "BFF2X3AF-BK-RX", "FM87X28OC-BK-RX", "FM87X24LN-RX", "FM0X25TP-RX",
            "GO47X57TK-BK-RX", "GO48X78SK-RX", "FM0X75PB-RX", "FM72X60MS-RX",
            "FM20X08EV-RX", "FM10X01ED-RX", "FM65X07DN-RX", "FM20X14DF-RX",
            "FM270X19DT-RX", "FM0X76AB-RX", "FM87X27SP-RX", "G081X24MT-RX",
            "GO00X47BB-RX",
        },
        "variable": {
            "vshield-flip-up-face-shield-w-25-mm-pet-transparent-visor",
            "7-eye-replacement-foam",
            "wiley-x-saint-for-rx-sm-lg",
        },
        "variation": {
            "LABEL-FEDEX2DAYS",
            "LABEL-UPSOVERNIGHT",
        },
    },
    "monster": {
        "simple": set(),
        "variable": {
            "prosport-vshield-flip-up-face-shield-w-25-mm-pet-transparent-visor",
        },
        "variation": set(),
    },
    "prosport": {
        "simple": set(),
        "variable": set(),
        "variation": set(),
    },
}

brand_removes = REMOVE.get(slug, {"simple": set(), "variable": set(), "variation": set()})
remove_simple    = brand_removes["simple"]
remove_variable  = brand_removes["variable"]
remove_variation = brand_removes["variation"]

items = json.loads(in_path.read_text())

out_dir = BASE / "data" / slug / "remove-items"
out_dir.mkdir(parents=True, exist_ok=True)

kept    = []
removed = []

for item in items:
    is_simple = item.get("sku") is not None

    if is_simple:
        if item["sku"] in remove_simple:
            removed.append(item["name"])
            continue
        kept.append(item)
    else:
        if item["slug"] in remove_variable:
            removed.append(item["name"])
            continue

        # drop flagged variations; re-check minimum count
        surviving = [v for v in item.get("variations", []) if v["sku"] not in remove_variation]
        if len(surviving) < len(item.get("variations", [])):
            if len(surviving) < 2:
                removed.append(item["name"])
                continue
            item = {**item, "variations": surviving}

        kept.append(item)

(out_dir / "items.json").write_text(json.dumps(kept, indent=2, ensure_ascii=False))
print(f"Kept: {len(kept)}  Removed: {len(removed)}")
for name in removed:
    print(f"  - {name}")
