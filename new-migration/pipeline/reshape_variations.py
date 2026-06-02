import html as html_mod
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE.parent / ".env")

BRAND_CONFIG = {
    "prosport": {"slug": "prosport"},
}

brand_name = os.getenv("BRAND")
config = BRAND_CONFIG.get(brand_name)
if not config:
    raise SystemExit(f"Unknown BRAND={brand_name!r}. Add it to BRAND_CONFIG.")

slug = config["slug"]

in_path = BASE / "data" / slug / "validate-variations" / "variations.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_variations.py first. Not found: {in_path}")

raw = json.loads(in_path.read_text())
out_dir = BASE / "data" / slug / "reshape-variations"
out_dir.mkdir(parents=True, exist_ok=True)

IMG_TAG_RE = re.compile(r'<img[^>]*>', re.IGNORECASE)
TAG_RE     = re.compile(r'<[^>]+>')

def strip_html(text):
    if not text:
        return None
    text = IMG_TAG_RE.sub(' ', text)
    text = TAG_RE.sub(' ', text)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text or None

def to_cents(val):
    if val in (None, ''):
        return None
    try:
        return round(float(val) * 100)
    except (TypeError, ValueError):
        return None

def to_num(val):
    if val in (None, ''):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def clean_attr_name(name):
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    return name

def normalize_power(val):
    try:
        return f"{float(val.replace('-', '.')):.2f}"
    except (ValueError, AttributeError):
        return val

def reshape(v):
    # stock
    sq = v.get('stock_quantity')
    stock = sq if sq is not None else (1 if v.get('stock_status') == 'instock' else 0)

    # dimensions: always an object; fields null if missing
    dims = v.get('dimensions') or {}
    l, w, h = to_num(dims.get('length')), to_num(dims.get('width')), to_num(dims.get('height'))
    dimensions = {'length': l, 'width': w, 'height': h}

    return {
        'id':               v['id'],
        'parent_id':        v['parent_id'],
        'name':             v.get('name'),
        'type':             v.get('type'),
        'oldUrl':          v.get('permalink'),
        'description':      strip_html(v.get('description')),
        'sku':              v['sku'],
        'regularPriceCents': to_cents(v.get('regular_price')),
        'salePriceCents':   to_cents(v.get('sale_price')),
        'sale':             v.get('on_sale'),
        'stock':            stock,
        'weight':           to_num(v.get('weight')),
        'dimensions':       dimensions,
        'images':           [v['image']] if v.get('image') and v['image'].get('src') else [],
        'attributes':       [
            {'name': clean_attr_name(a['name']), 'option': normalize_power(a['option']) if clean_attr_name(a['name']) == 'Power' else a['option']}
            for a in v.get('attributes', [])
        ],
    }

reshaped = [
    {'product_id': entry['product_id'], 'variations': [reshape(v) for v in entry['variations']]}
    for entry in raw
]

out_path = out_dir / 'variations.json'
out_path.write_text(json.dumps(reshaped, indent=2, ensure_ascii=False))

total = sum(len(e['variations']) for e in reshaped)
print(f'Reshaped {total} variations across {len(reshaped)} products → {out_path}')
