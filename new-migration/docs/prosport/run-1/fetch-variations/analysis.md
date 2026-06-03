# fetch-variations analysis — run 1 (proSPORT Sunglasses)
_2026-06-02_

Identical to build-run analysis. See `docs/build-run/fetch-variations/analysis.md` for full breakdown.

## Summary

| | |
|---|---|
| Variable products | 153 |
| Total variations | 1,758 |
| Min per product | 2 |
| Max per product | 88 (Jersey Sunglass Readers) |
| Avg per product | 11.5 |
| All status=publish | 1,758/1,758 |
| All have image | 1,758/1,758 |
| Has price | 1,757/1,758 |
| on_sale=True with sale_price | 1,757/1,757 |
| manage_stock=True | 1,758/1,758 |
| instock | 1,434 |
| outofstock | 324 |
| Has weight | 1,757/1,758 |
| Has description | 429/1,758 |

No anomalies vs build-run.

## Note

Two 503 errors on first pass (id=1894, id=1657). Crash-safe resume resolved both. No impact on final data.
