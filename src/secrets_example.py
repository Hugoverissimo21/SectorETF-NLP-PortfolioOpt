"""Template for private credentials — copy to `src/secrets.py` and fill in.

`src/secrets.py` is gitignored; never commit real keys. Notebooks that need
a credential import it as `from src.secrets import <NAME>`.

Credentials used by this project:
- IAEDU_API_KEY: api.iaedu.pt agent-chat endpoint (optional; only for the
  commented LLM-call snippets in 01_data/processed/build_model_inputs.ipynb).
- GOOGLE_APPLICATION_CREDENTIALS_PATH: path to a GCP service-account JSON
  with BigQuery access, needed to re-run the GDELT queries in
  01_data/news_collection.ipynb.
- HF_TOKEN: Hugging Face access token, needed to download gated models for
  the LLM labeling notebooks (02_sentiment/labeling/).
"""

IAEDU_API_KEY = "your-key-here"
GOOGLE_APPLICATION_CREDENTIALS_PATH = "/path/to/your/gcp-service-account.json"
HF_TOKEN = "hf_your-token-here"
