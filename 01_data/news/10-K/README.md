# 10-K filings (contents gitignored)

This folder holds one JSON per S&P 500 company with its latest 10-K filing
text — **309 files, ~421 MB, named by SEC CIK** (e.g. `0000001800.json`).
They are excluded from the repo for size reasons.

One example filing (`0000001800.json`) is tracked so you can see the
expected structure without downloading anything.

To populate the rest, run the 10-K download cells in
[`../../news_collection.ipynb`](../../news_collection.ipynb) — they fetch
the filings from SEC EDGAR using `../company_tickers.json` and write them
here, exactly where the downstream dictionary-building cells expect them.
