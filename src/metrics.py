"""Portfolio performance and risk metrics.

Was `experiments/portfolio/utils/PortfolioMetrics.py` (duplicated verbatim in
`results/utils/`); now the single copy, with the hardcoded absolute default
paths replaced by src.config constants. Used by all 03_portfolio training /
benchmark notebooks and the 04_results analysis notebooks
(`from src.metrics import PortfolioMetrics`).
"""

import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

from src import config
from src.data import SECTOR_ETFS, build_adj_close_matrix, load_etfs


class PortfolioMetrics:
    """
    Compute portfolio performance and risk metrics from time-series asset returns.

    This class expects the ETF price data to be provided via a pickle file
    (default: 01_data/processed/etfs_0.pkl, see src.config.ETFS_PKL) and
    computes returns internally. The instance is configured to work with a
    fixed returns matrix of shape (500, 11) and all metric methods accept a
    weights array of that same shape (no date slicing).

    Expects the 11 SPDR sector ETFs:
    ['XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY']

    Takes into account bid-ask spreads for trading cost calculations, using a
    JSON file (source: https://www.ssga.com/us/en/intermediary) and a
    risk-free rate CSV for Sharpe ratio calculations
    (source: https://fred.stlouisfed.org/series/DGS1MO).

    NOTE — hard constraints, by design: exactly 500 trading days of returns
    from 2023-07-01 onward and exactly 11 assets. Regenerating etfs_0.pkl
    with fresh yfinance data outside that window will raise on init.
    """

    def __init__(self,
                 etfs_data: str = str(config.ETFS_PKL),
                 bid_ask_spreads: str = str(config.BID_ASK_JSON),
                 risk_free_rate: str = str(config.TBILLS_CSV),
                 periods_per_year: int = 252):

        self.ppy = periods_per_year
        self.expected_order = list(SECTOR_ETFS)

        etfs = load_etfs(etfs_data)
        prices = build_adj_close_matrix(etfs, self.expected_order)
        returns = prices.pct_change()["2023-07-01":]

        if returns.shape[0] != 500:
            raise ValueError(f"Return rows: {returns.shape[0]} != 500 trading days")
        if returns.shape[1] != 11:
            raise ValueError(f"Unexpected number of assets: {returns.shape[1]} != 11 sectors")

        self.returns = returns
        self.assets = list(returns.columns)

        with open(bid_ask_spreads, "r") as f:
            spreads_dict = json.load(f)

        self.spreads = np.array([spreads_dict[t] for t in self.expected_order])

        self.rf = (pd.read_csv(risk_free_rate)
           .set_index("observation_date")
           .pipe(lambda df: df.loc["2023-07-01":])
           .rename_axis(None)
           .pipe(lambda s: pd.to_datetime(s.index).to_series(index=s.index).pipe(lambda _: s.set_axis(pd.to_datetime(s.index))))
           .reindex(self.returns.index.tz_localize(None))
           .ffill()).values / 100

    def _validate_inputs(self, weights):
        expected_shape = (500, 11)
        if weights.shape != expected_shape:
            raise ValueError(f"weights shape {weights.shape} invalid (expected {expected_shape})")
        if weights.shape != self.returns.shape:
            raise ValueError(f"weights shape {weights.shape} does not match returns shape {self.returns.shape}")
        if not np.allclose(weights.sum(axis=1), 1.0):
            raise ValueError("weights do not sum to 1 along axis 1")
        return self.returns.values

    def _portfolio_returns(self, weights):
        r = self._validate_inputs(weights)

        gross_pr = np.sum(weights * r, axis=1)

        delta_w = np.diff(weights, axis=0, prepend=weights[0:1])
        cost_matrix = np.abs(delta_w) * (self.spreads / 2)
        trading_cost = np.sum(cost_matrix, axis=1)

        net_pr = gross_pr - trading_cost

        return net_pr

    def _cumulative_returns_overtime(self, weights):
        pr = self._portfolio_returns(weights)
        return np.cumprod(1 + pr)

    def cumulative_return(self, weights):
        pr = self._portfolio_returns(weights)
        return np.prod(1 + pr) - 1

    def volatility(self, weights):
        pr = self._portfolio_returns(weights)
        return np.std(pr) * np.sqrt(self.ppy)

    def sharpe_ratio(self, weights):
        pr = self._portfolio_returns(weights)
        excess = pr - self.rf / self.ppy
        return np.mean(excess) / (np.std(excess) + 1e-8) * np.sqrt(self.ppy)

    def max_drawdown(self, weights):
        pr = self._portfolio_returns(weights)
        cum = np.cumprod(1 + pr)
        peak = np.maximum.accumulate(cum)
        dd = (cum - peak) / peak
        return dd.min()

    def summary(self, weights):
        return {
            "cumulative_return": self.cumulative_return(weights),
            "volatility": self.volatility(weights),
            "sharpe_ratio": self.sharpe_ratio(weights),
            "max_drawdown": self.max_drawdown(weights),
        }

    def plot_weights(self, weights):
        fig, ax = plt.subplots(figsize=(14, 6))

        ax.stackplot(
            np.arange(500),
            weights.T,
            labels=self.expected_order,
            alpha=0.9
        )

        ax.set_xlim(0, 499)
        ax.set_ylim(0, 1)
        ax.set_xlabel("Time (Days)")
        ax.set_ylabel("Weight (%)")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            frameon=False
        )

        ax.set_title("Sector Composition Over Time")

        plt.tight_layout()
        plt.show()

    def plot_cumulative_returns(self, weights):
        cum = self._cumulative_returns_overtime(weights)

        fig, ax = plt.subplots(figsize=(14, 5))

        ax.plot(
            cum,
            color="black",
            linewidth=2
        )

        ax.set_xlim(0, len(cum) - 1)
        ax.set_xlabel("Time (Days)")
        ax.set_ylabel("Portfolio Value")

        ax.set_title("Cumulative Portfolio Return Over Time")

        ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

        plt.tight_layout()
        plt.show()
