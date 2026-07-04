"""Central configuration: project paths.

Replaces the hardcoded absolute paths (/Users/...) that previously lived in
every notebook. Used by every stage of the pipeline and by the other src/
modules (metrics, data, plotting). Random seeds live in src/seeds.py.

All paths are relative to the repository root, which is located from this
file's position — no environment variables or editable-install required for
path resolution (though `pip install -e .` is the supported way to make
`import src` work from any notebook).
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------- directories
DATA_DIR = PROJECT_ROOT / "01_data"
PROCESSED_DIR = DATA_DIR / "processed"
AUX_DIR = DATA_DIR / "aux"
NEWS_DATA_DIR = DATA_DIR / "news"
REDDIT_DATA_DIR = DATA_DIR / "reddit"

SENTIMENT_DIR = PROJECT_ROOT / "02_sentiment"
LABELING_DIR = SENTIMENT_DIR / "labeling"
SENTIMENT_NEWS_DIR = SENTIMENT_DIR / "news"
SENTIMENT_REDDIT_DIR = SENTIMENT_DIR / "reddit"

PORTFOLIO_DIR = PROJECT_ROOT / "03_portfolio"

RESULTS_DIR = PROJECT_ROOT / "04_results"
WEIGHTS_DIR = RESULTS_DIR / "weights"

THESIS_DIR = PROJECT_ROOT / "thesis"
FIGS_DIR = THESIS_DIR / "figs"

# ---------------------------------------------------------------- key files
ETFS_PKL = PROCESSED_DIR / "etfs_0.pkl"          # ETF prices used everywhere downstream
ETFS_RAW_PKL = DATA_DIR / "etfs_data.pkl"        # raw yfinance download
REDDIT_PARQUET = REDDIT_DATA_DIR / "reddit.parquet"       # raw dump (gitignored, see 01_data/README)
REDDIT_0_PARQUET = PROCESSED_DIR / "reddit_0.parquet"     # filtered (gitignored, rebuilt by build_model_inputs.ipynb)
NEWS_0_JSON = PROCESSED_DIR / "news_0.json"
TENK_DIR = NEWS_DATA_DIR / "10-K"                # SEC filings (gitignored, re-download via news_collection.ipynb)

BID_ASK_JSON = AUX_DIR / "bid-ask_spread.json"   # source: ssga.com
TBILLS_CSV = AUX_DIR / "1M_TBills.csv"           # source: FRED DGS1MO
NON_TRADABLE_DAYS = AUX_DIR / "non_tradable_days.txt"

PORTFOLIO_DATASET = PORTFOLIO_DIR / "dataset.parquet"

# Random seeds live in src/seeds.py (one named constant per notebook,
# original values preserved).
