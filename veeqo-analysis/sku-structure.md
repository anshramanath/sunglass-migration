# SKU Structure
_Verified across BikerShades, ProSport, Monster — 2026-06-05_

---

## Format

```
[C] TYPE NNXnn [SUFFIX] - ATTR1 - ATTR2 - ATTR3 - ATTR4
 │   │    └──┘    │
 │   │    model   └─ optional variant type (PL, CP, ...)
 │   └─ product category
 └─ optional: C = combo / 2-pack
```

### Type prefixes

| Prefix | Category |
|---|---|
| `CA` | Classic / Acetate |
| `SP` | Sport |
| `BF` | Bifocal |
| `GO` | Goggle |
| `FM` | Foam-padded |
| `RE` | Reader |
| `SRE` | Sun Reader |
| `MAR` | Mariner |
| `LO` | Locs |
| `PL` | Polarized (standalone) |
| `PR` | ProSport |
| `COMP` | Computer glasses |
| `ACCS` | Accessories |

### Model number — `NNXnn`

The number in the first chunk is the manufacturer's model number with an `X` inserted to obscure it from channel scrapers and competitors. `CA10X16` = model `1016`, `BF2X6KT` = model `26` (with frame suffix `KT`).

The `X` is a deliberate encoding convention, not a structural separator.

### Suffix (optional)

Appended directly to the model number within the first chunk:

| Suffix | Meaning |
|---|---|
| `PL` | Polarized |
| `CP` | Combo Polarized |
| `KT` | Frame style (e.g. Kumatage) |
| `GT`, `RT`, etc. | Model name abbreviation |

### C-prefix — combo / 2-pack

A leading `C` before the type prefix means the SKU is a combo (2-pack) of the base product:

```
CA60X17MB-BK-SM       → single
CCA60X17MB-BKSMxBKSM  → combo (2x CA60X17MB)

CPR29X37GT-BKCLXTOCL  → combo ProSport
PR29X37GT-BK-CL       → single ProSport
```

The pipeline's C-prefix normalization strips one leading `C` before comparing bases, so combos and singles are correctly treated as the same product family.

---

## Verification

Checked all variable products across all three brands (veeqo-items stage):

| Brand | Consistent | Inconsistent | No X-pattern |
|---|---|---|---|
| BikerShades | 330 | **0** | 99 |
| ProSport | 135 | **0** | 3 |
| Monster | 220 | **0** | 10 |

Zero inconsistencies. Every variable product using the house SKU format has the same `NNXnn` model number across all its variations.

**Conclusion:** a mismatch in the model number between two SKUs is a definitive signal that they belong to different product families and should not be in the same group.

---

## Exceptions — third-party brands

The "no X-pattern" products use their own SKU conventions and are not subject to this rule:

| Brand | Format | Example |
|---|---|---|
| Wiley X | `WX-MODELNAME-...` | `WX-HUDSON-MBK-XTCLEARTOBROWNNO-MFB` |
| X-Loop | `XP8XHDnnnn-...` | `XP8XHD3320-BKOR-HD` |
| Alpine | `SP-MODELNAME-...` | `SP-Alpine-BK-SM` |

These are reseller/third-party products with externally assigned SKUs. The model number rule does not apply to them.

---

## Implications for the pipeline

- **Base mismatch check** — splitting on `-` and comparing the first chunk is the correct granularity. Any difference in the first chunk (after C-prefix normalization) = different product family = the group is wrong.
- **Sellbrite audit** — the 31 flagged Sellbrite variation groups confirmed: every mismatch is a genuinely different model number, not a formatting variation.
- **WooCommerce pipeline** — the 72/114/653 base mismatch variations flagged at validate_variations are all real errors — different model families grouped under one WooCommerce variable product.
