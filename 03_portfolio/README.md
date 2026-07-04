# 03_portfolio — allocation models & benchmarks

Third pipeline stage: allocate across the 11 GICS sector ETFs using the
sentiment features, and compare against benchmarks.

## Dataset

`dataset.ipynb` merges technical features with the news/Reddit sentiment
features from `02_sentiment/*/as_feature/` into `dataset.parquet`
(feature list: `dataset_features.txt`). Trading-day alignment uses
`01_data/aux/non_tradable_days.txt`.

## Strategies

Each strategy has a main (technical-only) notebook plus three feature
variants (`*_reddit`, `*_news`, `*_reddit+news`). Version numbers reflect
the iteration that made it into the thesis:

| Strategy (thesis name) | Final version | Folder |
|---|---|---|
| **DRL–PPO** — Deep RL agent (PPO, stable-baselines3) | v9.1.3 / v9.1.X variants | `DRL_PPO/` (run dirs `v913*/` keep optuna + eval artifacts) |
| **LSTM–SR** — end-to-end LSTM maximizing the Sharpe ratio | v3.2.2 / v3.2.X variants | `LSTM_sharpe/` (run dirs `v322*/`) |
| **LSTM–BL** — LSTM ensemble for return prediction + Black-Litterman construction | v5.2.2 / v5.2.X variants | `LSTM_returns/` (run dirs `v522*/`; `_v522_returns_prediction/` has prediction metrics) |

## Benchmarks (`benchmarks/`)

- `MVO_CAPM/` — mean-variance optimization with CAPM expected returns
  (uses the longer risk-free history `01_data/aux/1M_TBills_full_history.csv`)
- `EW/` — equal weight
- `SP500/` — S&P 500 buy-and-hold

## Weights

Training notebooks save their `*_weights.npy` **next to the notebook**
(so re-runs never clobber the thesis artifacts); the **canonical weights
used in the thesis live in `04_results/weights/`**. Evaluation everywhere
uses `src.metrics.PortfolioMetrics` (net of bid-ask trading costs).

Seeds per notebook are in `src/seeds.py` (values unchanged from the
original runs). Exact environments: `envs/03_drl_ppo.yml`, `envs/03_lstm.yml`,
`envs/03_mvo_capm.yml`, and `envs/03_portfolio_base.yml` (dataset assembly,
EW/SP500 benchmarks, results).
