# Missing Attributes Review

Source: `migration/reshaped/missing_attributes_products_shape.json`

These products were flagged during reshaping for missing attributes and need manual review before migration.

For this bucket, the decision path is straightforward: take every item to the owner. The issue here is that some variations are missing usable option metadata in both the reshaped `attribute` field and the nested variation `variation` field, so we cannot recover them confidently without owner input.

## Checklist

- [ ] Magnum – Clear
- [ ] Locs Impala 91025
- [ ] Seaway
- [ ] Aruba Polarized Sunglasses
- [ ] Taxi Polarized Bifocal [Fits MEDIUM -XLARGE Heads]
- [ ] Starlet Over Sized Fashion Bifocal
- [ ] Finish Line Bifocal [Fits MEDIUM – XLARGE Heads]

## Review Table

| Name | Product ID | SKU | Variations | Decision |
| --- | ---: | --- | ---: | --- |
| Magnum – Clear | 49023 | `FM85X11MNM-0-CL` | 36 | Ask owner |
| Locs Impala 91025 | 34373 | `LO91025-0` | 4 | Ask owner |
| Seaway | 30744 | `CAPL14X64SW-0` | 4 | Ask owner |
| Aruba Polarized Sunglasses | 30237 | `PL290X91AR-0` | 10 | Ask owner |
| Taxi Polarized Bifocal [Fits MEDIUM -XLARGE Heads] | 13112 | `BFPL58X852TX-0` | 22 | Ask owner |
| Starlet Over Sized Fashion Bifocal | 10264 | `BF4X30ST-0` | 16 | Ask owner |
| Finish Line Bifocal [Fits MEDIUM – XLARGE Heads] | 6507 | `BF79X89FL-0` | 12 | Ask owner |

## Product Notes

### Magnum – Clear

- Product ID: `49023`
- SKU: `FM85X11MNM-0-CL`
- Variations: `36`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Locs Impala 91025

- Product ID: `34373`
- SKU: `LO91025-0`
- Variations: `4`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Seaway

- Product ID: `30744`
- SKU: `CAPL14X64SW-0`
- Variations: `4`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Aruba Polarized Sunglasses

- Product ID: `30237`
- SKU: `PL290X91AR-0`
- Variations: `10`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Taxi Polarized Bifocal [Fits MEDIUM -XLARGE Heads]

- Product ID: `13112`
- SKU: `BFPL58X852TX-0`
- Variations: `22`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Starlet Over Sized Fashion Bifocal

- Product ID: `10264`
- SKU: `BF4X30ST-0`
- Variations: `16`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:

### Finish Line Bifocal [Fits MEDIUM – XLARGE Heads]

- Product ID: `6507`
- SKU: `BF79X89FL-0`
- Variations: `12`
- What it is:
- Missing attribute issue:
- Decision: `ask-owner`
- Action / Notes:
