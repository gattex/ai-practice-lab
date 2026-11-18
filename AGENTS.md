# AGENTS.md

## Project

AI Practice Lab is a personal repo for studying AI with real model APIs. The main component is `email_classifier.py`, which classifies support emails for an online sneaker store using Google Gemini.

## Layout

- `email_classifier.py`: the classifier. Reads `emails/*.txt`, calls Gemini, prints a category and summary.
- `emails/`: sample email inputs (`.txt`). Plain text, UTF-8.
- `README.md`: user-facing setup and run instructions.
- Other top-level `.py` files (`app.py`, `modelos.py`, `prueba.py`, `rag.py`) are experiments not yet documented. Don't modify them unless asked.

## Setup and run

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-genai pydantic
export GEMINI_API_KEY="..."
python email_classifier.py   # run from the repo root
```

The script uses a relative path (`Path("emails")`), so it must run from the repo root.

## Conventions

- The API key comes from the `GEMINI_API_KEY` environment variable. Never hardcode keys or commit `.env` files.
- The model name lives in the `MODEL` constant. Keep it in one place.
- Classification output is validated with the Pydantic `Classification` model through `response_schema`. Keep the categories in sync between the `Literal` type and the `RULES` prompt.
- Keep `temperature=0` for classification so results are consistent.
- Retry only on `errors.ServerError` (5xx). Do not retry `errors.ClientError` (4xx).
- Comments and the README are in English. Email content and categories come from the Spanish-speaking domain examples; keep the prompt rules as they are unless asked to change them.

## Working in this repo

- It's a learning repo: prefer small, readable changes over abstractions.
- There is no test suite or `requirements.txt` yet. If you add one, say so in the summary.
- Don't commit or push unless asked.
- `venv/` and `__pycache__/` are ignored by git. Don't add them.
