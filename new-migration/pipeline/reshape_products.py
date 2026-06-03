import html as html_mod
import json
import os
import sys
import re
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import BASE, load_brand


brand_key, config = load_brand()
slug       = config["slug"]
brand_name = config["brand_name"]

in_path = BASE / "data" / slug / "validate-products" / "products.json"
if not in_path.exists():
    raise SystemExit(f"Run validate_products.py first. Not found: {in_path}")

data = json.loads(in_path.read_text())
out_dir = BASE / "data" / slug / "reshape-products"
out_dir.mkdir(parents=True, exist_ok=True)

def image_name(src):
    return urlparse(src).path.rstrip('/').rsplit('/', 1)[-1] or 'image.jpg'

IMG_RE     = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
IMG_TAG_RE = re.compile(r'<img[^>]*>', re.IGNORECASE)
LI_RE  = re.compile(r'<li>(.*?)</li>', re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')

ATTR_OVERRIDES = {
    "monster": {
        "Cleaner Spray Bottle QTY":  "Quantity",
        "Qty":                       "Quantity",
        "Frame Styles for Filter":   "Style",
        "Special Size for Filter":   "Size",
    },
}

def clean_attr_name(raw):
    override = ATTR_OVERRIDES.get(brand_key, {}).get(raw)
    if override:
        return override
    name = re.sub(r'(?i)\s+for\s+filter$', '', raw).strip()
    name = re.sub(r'(?i)^choose\s+', '', name).strip()
    name = re.sub(r'(?i)^filter\s+by\s+', '', name).strip()
    name = re.sub(r'\s*\(.*?\)', '', name).strip()
    return name

def normalize_power(val):
    try:
        return f"{float(val.replace('-', '.')):.2f}"
    except (ValueError, AttributeError):
        return val

def strip_html(text):
    if not text:
        return None
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

def reshape(p):
    is_variable = p['type'] == 'variable'

    # description: extract img URLs, strip all HTML to plain text
    desc_raw = p.get('description') or ''
    desc_imgs = [{'src': url, 'name': image_name(url)} for url in IMG_RE.findall(desc_raw)]
    desc_text = strip_html(IMG_TAG_RE.sub('', desc_raw))

    # short_description: parse <li> items to plain text array
    sd_raw = p.get('short_description') or ''
    bullets = [html_mod.unescape(TAG_RE.sub('', li)).strip() for li in LI_RE.findall(sd_raw)]
    short_desc = [b for b in bullets if b] or None

    # pricing
    if is_variable:
        # min/max and salePriceCents deferred to combine step
        min_price = max_price = sale_price = None
        sale = p.get('on_sale')
    else:
        rp = to_cents(p.get('regular_price'))
        base = rp if rp is not None else to_cents(p.get('price'))
        min_price = max_price = base
        sale_price = to_cents(p.get('sale_price'))
        sale = p.get('on_sale')

    # stock: variable products defer to variation-level stock; simple products use quantity or status fallback
    if is_variable:
        stock = None
    else:
        sq = p.get('stock_quantity')
        stock = sq if sq is not None else (1 if p.get('stock_status') == 'instock' else 0)

    # dimensions: always an object; fields null if missing
    dims = p.get('dimensions') or {}
    l, w, h = to_num(dims.get('length')), to_num(dims.get('width')), to_num(dims.get('height'))
    dimensions = {'length': l, 'width': w, 'height': h}

    return {
        'id':                p['id'],
        'name':              p['name'],
        'slug':              p['slug'],
        'oldUrl':           p['permalink'],
        'type':              p['type'],
        'description':       desc_text,
        'descriptionImages': desc_imgs,
        'summary':  short_desc or [],
        'sku':               p['sku'],
        'minPriceCents':     min_price,
        'maxPriceCents':     max_price,
        'salePriceCents':    sale_price,
        'sale':              sale,
        'featured':          p.get('featured'),
        'totalSales':        p.get('total_sales') or 0,
        'stock':             stock,
        'weight':            to_num(p.get('weight')),
        'dimensions':        dimensions,
        'categories':        p.get('categories', []),
        'images':            p.get('images', []),
        'attributes':        [
            {
                **a,
                'name':    clean_attr_name(a['name']),
                'options': [normalize_power(o) if clean_attr_name(a['name']) == 'Power' else o for o in a.get('options', [])],
            }
            for a in p.get('attributes', [])
        ],
        'variations':        p.get('variations', []),
    }

reshaped = [reshape(p) for p in data]

out_path = out_dir / 'products.json'
out_path.write_text(json.dumps(reshaped, indent=2, ensure_ascii=False))

print(f'Reshaped {len(reshaped)} products → {out_path}')
