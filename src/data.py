"""Data loading helpers shared across the pipeline.

Absorbs the pickle/parquet loading boilerplate that was repeated in the
portfolio dataset notebook, the benchmark notebooks and the results
notebooks. Used by 03_portfolio/* and 04_results/* notebooks and by
src.metrics.PortfolioMetrics.
"""

import json
import pickle

import pandas as pd

from src import config

# the 11 SPDR sector ETFs used throughout the thesis, in canonical order
SECTOR_ETFS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK",
               "XLP", "XLRE", "XLU", "XLV", "XLY"]


def load_etfs(path=config.ETFS_PKL):
    """Load the ETF price dict ({ticker: {"data": DataFrame, ...}})."""
    with open(path, "rb") as f:
        return pickle.load(f)


def build_adj_close_matrix(etfs, tickers=SECTOR_ETFS):
    """Adjusted-close price matrix (dates x tickers), NaN rows dropped.

    Lifted from the old PortfolioMetrics.__init__.
    """
    price_series = []
    for ticker in tickers:
        df = etfs[ticker]["data"].copy()
        s = df["Adj Close"].rename(ticker)
        price_series.append(s)
    return pd.concat(price_series, axis=1).dropna()


def load_returns(start="2023-07-01", path=config.ETFS_PKL):
    """Daily pct-change returns of the sector ETFs from `start` onward."""
    prices = build_adj_close_matrix(load_etfs(path))
    return prices.pct_change()[start:]


def load_portfolio_dataset(path=config.PORTFOLIO_DATASET):
    """The merged features dataset built by 03_portfolio/dataset.ipynb."""
    return pd.read_parquet(path)


def load_bid_ask_spreads(path=config.BID_ASK_JSON):
    with open(path) as f:
        return json.load(f)


def load_non_tradable_days(path=config.NON_TRADABLE_DAYS):
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]
