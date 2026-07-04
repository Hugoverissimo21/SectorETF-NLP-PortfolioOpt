"""Thesis-styled matplotlib setup and shared portfolio figures.

Was `results/utils/cumret_e_weights.py`; the LaTeX/Latin-Modern rcParams
block that was also repeated inline across the 04_results notebooks now
lives in `setup_matplotlib()`. Used by 04_results/* notebooks and any
notebook that saves figures into thesis/figs.

Call `setup_matplotlib()` once per notebook (use `usetex=False` on machines
without a LaTeX installation — figures then render with mathtext instead).
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from src import config

# populated lazily by _pm() / _dataset() so importing this module stays cheap
_PM = None
_DATASET = None

ASSETS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK",
          "XLP", "XLRE", "XLU", "XLV", "XLY"]


def setup_matplotlib(usetex=True, dpi=600):
    """Match the thesis typography: Latin Modern via LaTeX rendering.

    usetex=True requires a LaTeX installation with lmodern; pass
    usetex=False for a dependency-free approximation.
    """
    params = {
        "text.usetex": usetex,
        "font.family": "serif",
        "font.size": 11,
        "axes.titlesize": 11,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": dpi,
    }
    if usetex:
        params.update({
            # Latin Modern — matches \usepackage{lmodern} in the thesis
            "font.serif": ["Latin Modern Roman"],
            "font.sans-serif": ["Latin Modern Sans"],
            "font.monospace": ["Latin Modern Mono"],
            "pgf.preamble": "\n".join([
                r"\usepackage[utf8]{inputenc}",
                r"\usepackage[T1]{fontenc}",
                r"\usepackage{lmodern}",
            ]),
        })
    mpl.rcParams.update(params)


def _pm():
    global _PM
    if _PM is None:
        from src.metrics import PortfolioMetrics
        _PM = PortfolioMetrics()
    return _PM


def _dataset():
    global _DATASET
    if _DATASET is None:
        _DATASET = pd.read_parquet(config.PORTFOLIO_DATASET)
    return _DATASET


def plot_portfolio_performance(weights, approach_name, variant_name,
                               ylim_cumret=None, save_path=None):
    """Cumulative return line + sector-weight stackplot on twin axes."""
    cumret = _pm()._cumulative_returns_overtime(weights)  # (500,)
    dates_plot = _dataset().index[-500:]                  # (500,)

    fig, ax1 = plt.subplots(figsize=(5.71 * 1.5, 3.5 * 1.2))

    ax1.plot(
        dates_plot,
        cumret,
        color="black",
        linewidth=2.5,
        label="CUMRET",
        zorder=10
    )

    ax1.set_ylabel("Cumulative Return (CUMRET)", color="black")
    ax1.tick_params(axis='y', labelcolor="black")

    ax2 = ax1.twinx()

    ax2.stackplot(
        dates_plot,
        weights.T,
        labels=ASSETS,
        alpha=0.35
    )

    ax2.set_ylim(0, 1)
    ax2.set_ylabel("Weights")
    ax2.tick_params(axis='y')

    fig.autofmt_xdate()

    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.set_title("Portfolio Performance and Weights - " + approach_name + " (" + variant_name + ")")

    ax1.margins(x=0)
    ax2.margins(x=0)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    ax1.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper left",
        bbox_to_anchor=(1.1, 1),
        borderaxespad=0
    )

    ax1.set_xlim(pd.Timestamp("2023-07-01"), pd.Timestamp("2025-07-01"))

    if ylim_cumret is not None:
        ax1.set_ylim(ylim_cumret)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
