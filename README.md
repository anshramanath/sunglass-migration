# 🕶️ Bikershades Migration

Migrating product data from the bikershades.com WordPress/WooCommerce store into a clean, normalized schema for a new app.

---

## 📦 What's in here

| File | Description |
|---|---|
| `migration/fetch_products.py` | Fetches all 647 products from the WooCommerce API |
| `migration/fetch_variations.py` | Fetches all 6,064 product variations |
| `migration/reshape_products.py` | Cleans and normalizes the raw data into a lean schema |
| `PROGRESS.md` | Full migration log — decisions, findings, field mappings |

---

## 🔄 Migration Pipeline

```
WooCommerce Store API
        ↓
products.json          ← raw backup of all products
        ↓
variations.json        ← raw backup of all variations
        ↓
reshape_products.py    ← normalize, clean, merge
        ↓
clean_products.json    ← ready for import
        ↓
download images        ← rehost to your own storage
        ↓
insert into DB         ← your new app reads from here
```

---

## 🚀 Running the scripts

**1. Install dependencies**
```bash
pip install requests
```

**2. Fetch all products**
```bash
cd migration
python fetch_products.py
```

**3. Fetch all variations**
```bash
python fetch_variations.py
```
> ✅ Crash-safe — resumes exactly where it left off if interrupted.

**4. Reshape into clean schema**
```bash
python reshape_products.py
```

---

## 📊 Catalog Stats

| | Count |
|---|---|
| Total products | 647 |
| Variable products | 489 |
| Simple products | 157 |
| Total variations | 6,064 |
| Clean products (after filtering) | 639 |
| Products on sale | 524 |

---

## 🗂️ Clean Product Shape

```json
{
  "name": "Backspin Sport Sunglasses",
  "slug": "backspin-sport-sunglasses",
  "sku": "SP47X96BS-0",
  "wpUrl": "https://bikershades.com/shop/...",
  "productUrl": "https://bikershades.com/wp-json/wc/store/products/67767",
  "description": "Capture the essence of athletic performance...",
  "descriptionImgs": ["https://bikershades.com/wp-content/uploads/diagram.jpg"],
  "summary": ["Fits Large to X-Large heads", "Impact resistant lenses"],
  "sale": true,
  "regularPriceInCents": 2599,
  "salePriceInCents": 1999,
  "averageRating": 4.5,
  "reviewCount": 12,
  "inStock": true,
  "categories": ["prosport-sunglasses", "smoke-grey"],
  "images": [{ "src": "https://...", "name": "Backspin Front" }],
  "attributes": ["blue-green-smoke", "glossy-black-green-smoke"],
  "variations": [
    {
      "attributes": ["blue-green-smoke"],
      "variation": { "...full variation object..." }
    }
  ],
  "weight": 2,
  "weightUnit": "oz",
  "dimensions": { "length": 6, "width": 3, "height": 3 },
  "dimensionUnit": "in"
}
```

---

## ✅ Progress

- [x] Fetch all products → `products.json`
- [x] Fetch all variations → `variations.json`
- [x] Reshape into clean schema → `clean_products.json`
- [ ] Download images locally
- [ ] Upload images to storage
- [ ] Insert into database
