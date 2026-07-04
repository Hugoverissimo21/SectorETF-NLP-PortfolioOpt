# 01_data — data collection & preparation

First pipeline stage: collect raw data (Reddit, news, SEC filings, ETF
prices) and turn it into the experiment-ready inputs in `processed/`.

## Notebooks

| Notebook | What it does |
|---|---|
| `reddit_collection.ipynb` | Downloads + filters the Reddit dump into `reddit/reddit.parquet` |
| `reddit_manual_labeling.ipynb` | Manual labeling workflow for a Reddit sample |
| `reddit/reddit_label_eda.ipynb` | EDA of the labeled sample |
| `news_collection.ipynb` | GICS sector dictionaries from SEC 10-K filings + GDELT BigQuery news extraction |
| `news_aux_gdelt_eda.ipynb` | GDELT v2 GKG exploration used to design filters |
| `news_aux_llm_keywords.ipynb` | LLM-assisted keyword augmentation for sector queries |
| `etfs_prices.ipynb` | Daily prices of the 11 SPDR sector ETFs via yfinance |
| `processed/build_model_inputs.ipynb` | Builds the `*_0` experiment inputs (etfs_0.pkl, news_0.json, reddit_0.parquet) |

## Data sources — how to obtain the excluded files

### Reddit dump (`reddit/reddit.parquet`, 976 MB, gitignored)

- Source: **Academic Torrents** (uploader RaiderBDev), monthly Reddit dumps:
  <https://academictorrents.com/details/30dee5f0406da7a353aff6a8caa2d54fd01f2ca1>
- Magnet: `magnet:?xt=urn:btih:30dee5f0406da7a353aff6a8caa2d54fd01f2ca1`
- `reddit_collection.ipynb` documents the exact download (aria2c) and the
  subreddit/date filtering that produces `reddit.parquet`
  (per-month message counts in `reddit/stats.json`).
- **`reddit/reddit_SAMPLE.parquet` ships in the repo**: the first 5 of
  705,601 rows, so you can inspect the schema
  (`top_comments`, `submission`, `subreddit`, `created_utc`) without
  downloading anything. Same idea for the filtered version:
  `processed/reddit_0_SAMPLE.parquet` (5 of 355,352 rows) — the full
  `reddit_0.parquet` is rebuilt by `processed/build_model_inputs.ipynb`.

### SEC 10-K filings (`news/10-K/*.json`, 309 files, 421 MB, gitignored)

Rebuilt by the download cells of `news_collection.ipynb`:

1. `news/company_tickers.json` (ships in the repo) maps S&P 500 tickers to
   SEC CIK numbers.
2. The notebook fetches each company's latest 10-K from **SEC EDGAR**
   (`https://www.sec.gov/cgi-bin/browse-edgar` / `data.sec.gov`) and stores
   one JSON per company in `news/10-K/` — see `news/10-K/README.md`.
3. Respect the SEC rate limit (10 req/s, declared User-Agent). Full
   download takes on the order of ~15–30 min.

Everything derived from the filings (TF-IDF dictionaries,
`gics_word_labeling_*.parquet`, `subind_words*.parquet`) already ships in
`news/`, so you only need the raw filings to re-derive those from scratch.

### GDELT news (BigQuery)

The news corpus comes from the **GDELT v2 GKG** public BigQuery dataset
(`gdelt-bq.gdeltv2.gkg`). You need your own GCP project + service account
with BigQuery access: copy `src/secrets_example.py` → `src/secrets.py` and
set `GOOGLE_APPLICATION_CREDENTIALS_PATH`. Queries and filtering are in
`news_collection.ipynb`; BigQuery billing applies (the GDELT table is large
— the notebook shows the sampled queries used).

### ETF prices

`etfs_prices.ipynb` downloads via **yfinance** (no credentials). The exact
snapshot used for the thesis ships as `etfs_data.pkl` /
`processed/etfs_0.pkl`, so downstream stages work offline out of the box.
Note: `src.metrics.PortfolioMetrics` asserts exactly 500 trading days from
2023-07-01 — a fresh download of a different window will fail its checks.

### aux/ — market reference data

| File | Source |
|---|---|
| `bid-ask_spread.json` | ssga.com (SPDR ETF pages) — used for trading costs |
| `1M_TBills.csv` | FRED `DGS1MO` (2021→) — risk-free rate for Sharpe |
| `1M_TBills_full_history.csv` | FRED `DGS1MO` (2015→) — longer window for MVO-CAPM |
| `non_tradable_days.txt` | derived — market holidays in the sample |
