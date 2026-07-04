# 02_sentiment — labeling & sentiment models

Second pipeline stage: label news/Reddit text with LLMs, train sector-aware
sentiment classifiers, and export sentiment as features for the portfolio
stage.

## labeling/

LLM labeling of the corpora, one parquet per batch, named
`{news|reddit}_{model}_{batch}_{hash}.parquet` (Qwen, Google Gemini,
Meta-Llama). Driven by `news_llm_labeling.ipynb` and
`reddit_llm_labeling.ipynb`. These batches ship in the repo — you don't need
to re-run labeling to train the models.

## news/ — news sentiment (per-sector)

Iterations tell the story; each has a training notebook per embedding
variant and a CV results folder:

| Iteration | Notebooks | CV output |
|---|---|---|
| v1 | `v1_{bert,tfidf,sector}_embeddings.ipynb` | `cv_results_v1/`, aggregated in `results_v1.ipynb` |
| v2 | `v2_{bert,tfidf,sector}_embeddings.ipynb` | `cv_results_v2/`, aggregated in `results_v2.ipynb` |
| **vf2 (final)** | `vf2_tfidf_embeddings.ipynb`, `vf2_sector_embeddings.ipynb` | run dirs `vf2_tfidf_embeddings/`, `vf2_sector_embeddings/` |

- `dataset.ipynb` assembles the training data from `../labeling/`;
  `hyperparameters.ipynb` defines the search space.
- The final model weights (`vf2_*/final_model.pt`, 418 MB each) are
  **gitignored** — retrain with the vf2 notebooks to regenerate them; the
  evaluation reports/confusion matrices in those folders ship in the repo.
- `as_feature/` runs the final model over the corpus and exports
  `as_feature_data.parquet` consumed by `03_portfolio/dataset.ipynb`.

## reddit/ — Reddit sentiment (ModernBERT multi-head)

| Iteration | Notebook | CV output |
|---|---|---|
| v1 / v2 | `v1_model.ipynb`, `v2_model.ipynb` | `cv_results_v1/`, `cv_results_v2/` |
| **v4 (final)** | `v4_model.ipynb` | `cv_results_v4/` |

- **THE thesis model is run `final_run_v4_h5a8a3d210b/`** — picked in
  `results.ipynb`, produced by the frozen code copy
  `h5a8a3d210b_full_run_code.ipynb` (data: `h5a8a3d210b_full_run_data.parquet`).
  Its `model.safetensors` (569 MB) is gitignored; metrics, learning curves
  and per-sector reports ship in the run folder.
- `dataset.ipynb` builds training data (`dataset.parquet`,
  `dataset_augmented.parquet`); `data_syntheticposts/` generates synthetic
  posts for validation; `as_feature/` exports the portfolio feature.

Training notebooks have outputs stripped (long logs); GPU strongly
recommended (see `envs/02_sentiment_gdelt.yml` and
`envs/02_sentiment_reddit.yml` for the exact environments;
`envs/02_labeling.yml` for the labeling notebooks).
