import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand

brand_key, config = load_brand()
slug = config["slug"]

in_path = BASE / "data" / slug / "normalize-images" / "items.json"
if not in_path.exists():
    raise SystemExit(f"Run normalize_image_names.py first. Not found: {in_path}")

items = json.loads(in_path.read_text())

COLOR_MAP = {
    # CSS named colors
    "black":     "#000000",
    "white":     "#ffffff",
    "red":       "#ff0000",
    "green":     "#008000",
    "blue":      "#0000ff",
    "yellow":    "#ffff00",
    "orange":    "#ffa500",
    "purple":    "#800080",
    "pink":      "#ffc0cb",
    "brown":     "#a52a2a",
    "gold":      "#ffd700",
    "silver":    "#c0c0c0",
    "gray":      "#808080",
    "grey":      "#808080",
    "violet":    "#ee82ee",
    "turquoise": "#40e0d0",
    "coral":     "#ff7f50",
    "salmon":    "#fa8072",
    "teal":      "#008080",
    "navy":      "#000080",
    "maroon":    "#800000",
    "crimson":   "#dc143c",
    "indigo":    "#4b0082",
    "lime":      "#00ff00",
    "cyan":      "#00ffff",
    "aqua":      "#00ffff",
    "magenta":   "#ff00ff",
    "fuchsia":   "#ff00ff",
    "beige":     "#f5f5dc",
    "ivory":     "#fffff0",
    "lavender":  "#e6e6fa",
    "tan":       "#d2b48c",
    "olive":     "#808000",
    "sienna":    "#a0522d",
    "peru":      "#cd853f",
    "chocolate": "#d2691e",
    "tomato":    "#ff6347",
    "wheat":     "#f5deb3",
    "khaki":     "#f0e68c",
    "plum":      "#dda0dd",
    "orchid":    "#da70d6",
    # custom sunglass colors
    "tortoise":  "#8b5e3c",
    "gunmetal":  "#2c3539",
    "clear":     "#e8f4f8",
    "copper":    "#b87333",
    "demi":      "#7b4a2d",
    "platinum":  "#e8e8e8",
    "charcoal":  "#36454f",
    "vanilla":   "#f3e5ab",
    "crystal":   "#d4eef5",
    "camo":      "#4b5320",
    "peach":     "#ffcba4",
    "bronze":    "#cd7f32",
    "burgundy":  "#800020",
    "carbon":    "#1c1c1c",
    "expresso":  "#3b1a08",
    "mahogany":  "#4e1609",
    "maple":     "#c8882a",
    "walnut":    "#4a3728",
}

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def derive_color(s):
    """First color word from the right in the slug; fallback hex if none found."""
    match = next((w for w in reversed(s.split("-")) if w in COLOR_MAP), None)
    return COLOR_MAP[match] if match else "#ffffff"


def enrich_option(raw, is_color):
    name = html.unescape(raw)
    s    = slugify(name)
    opt  = {"option": name, "slug": s}
    if is_color:
        opt["value"] = derive_color(s)
    return opt


for item in items:
    item["name"] = html.unescape(item["name"])

    for attr in (item.get("attributes") or []):
        attr["name"]    = html.unescape(attr["name"])
        is_color        = attr["name"] == "color"
        attr["options"] = [enrich_option(o, is_color) for o in (attr.get("options") or [])]

    for v in (item.get("variations") or []):
        for a in (v.get("attribute") or []):
            a["name"]   = html.unescape(a["name"])
            raw         = html.unescape(a["option"])
            s           = slugify(raw)
            a["option"] = raw
            a["slug"]   = s
            if a["name"] == "color":
                a["value"] = derive_color(s)

out_dir = BASE / "data" / slug / "decode-entities"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "items.json").write_text(json.dumps(items, indent=2, ensure_ascii=False))
print(f"Done. {len(items)} items written.")
