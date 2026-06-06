# Items to Remove

Products to be excluded before import. A script will read this list and strip them from the pipeline output.

Variations are matched by SKU. Variable products are matched by slug.

| Identifier | Type | Brand | Reason |
|---|---|---|---|
| LABEL-FEDEX2DAYS | Variation | BikerShades | Shipping service listing, not a sellable product |
| LABEL-UPSOVERNIGHT | Variation | BikerShades | Shipping service listing, not a sellable product |
| prosport-vshield-flip-up-face-shield-w-25-mm-pet-transparent-visor | Variable product | Monster | Two conflicting quantity attributes (Choose Quantity + Cleaner Spray Bottle QTY) — ambiguous structure |
| vshield-flip-up-face-shield-w-25-mm-pet-transparent-visor | Variable product | BikerShades | Two conflicting quantity attributes (Choose Quantity + Cleaner Spray Bottle QTY) — ambiguous structure |
| 7-eye-replacement-foam | Variable product | BikerShades | Third-party (non-house) brand product — discontinued per owner |
