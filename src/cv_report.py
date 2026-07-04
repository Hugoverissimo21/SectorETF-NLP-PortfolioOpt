"""Cross-validation result loading shared by the sentiment results notebooks.

Absorbs the JSON-directory loading loops that were duplicated across
02_sentiment/news/results_v1.ipynb, results_v2.ipynb (per-hyperparameter
fold tables, split by embedding prefix) and 02_sentiment/reddit/results.ipynb
(per-run CV summaries). Plot styling stays in the notebooks.
"""

import json
import os


def load_cv_json_dir(folder, prefix=None):
    """Merge every '{prefix}*.json' in `folder` into one {config: table} dict.

    News-style CV output: each JSON maps hyperparameter-config names to a
    {"columns": [...], "data": [...]} table with per-fold metrics.
    """
    results = {}
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        if prefix and not name.startswith(prefix):
            continue
        with open(os.path.join(folder, name)) as f:
            data = json.load(f)
        for cfg, table in data.items():
            results[cfg] = table
    return results


def load_cv_runs(folder, hide_hashes=()):
    """Reddit-style CV output: one JSON per run with mean CV macro-F1.

    Returns runs sorted by validation macro-F1 (descending).
    """
    hide = set(hide_hashes)
    runs = []
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(folder, name)) as f:
            d = json.load(f)
        h = d["hparams_hash"]
        if h in hide:
            continue
        runs.append({
            "hash": h,
            "train_f1": d["train_macro_f1_mean_cv"],
            "val_f1": d["val_macro_f1_mean_cv"],
            "hparams": d["hparams"],
        })
    runs.sort(key=lambda r: r["val_f1"], reverse=True)
    return runs
