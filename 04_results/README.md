# 04_results — analysis, figures, canonical weights

Final pipeline stage: compare all strategies and produce the thesis figures.

## Notebooks

| Notebook | Contents |
|---|---|
| `results_pt1.ipynb` | Main comparison across strategies × feature sets (metrics tables, radar) |
| `results_pt2.ipynb` | Cumulative-return + weights figure per strategy (heavy inline outputs stripped for the public repo — the rendered figures are in `thesis/figs/`, the fully-executed notebook is in the private archive) |
| `results_pt3.ipynb` | Additional analyses / robustness |
| `others/sentiment.ipynb`, `others/sentiment_p2.ipynb` | Sentiment-model results |
| `others/returns.ipynb` | Return-prediction results |
| `others/sota.ipynb` | Comparison with state-of-the-art references |

Figures for the document are saved into `thesis/figs/` (LaTeX-styled via
`src.plotting.setup_matplotlib()`; pass `usetex=False` if you don't have a
LaTeX installation).

## weights/

Canonical portfolio weight trajectories used in the thesis, one
`(500, 11)` `.npy` per strategy × feature set:
`{DRLPPO,LSTMvia-sharpe,LSTMvia-returns}_{technical,reddit,news,reddit+news}_weights.npy`
plus `EW_benchmark_weights.npy` and `MVOCAPM_benchmark_weights.npy`.
Produced by the `03_portfolio/` notebooks (which save locally when re-run —
copy here deliberately if you want to bless new runs). Evaluate any of them
with `src.metrics.PortfolioMetrics().summary(np.load(...))`.
