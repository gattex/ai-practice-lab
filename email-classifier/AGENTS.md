# AGENTS.md

## Project

AI Practice Lab is a personal repo for studying AI with real model APIs. The main component is `email_classifier.py`, which classifies support emails for an online sneaker store using Google Gemini.

## Layout

- `email_classifier.py`: the classifier. Reads `emails/*.txt`, calls Gemini, prints a category and summary.
- `emails/`: sample email inputs (`.txt`). Plain text, UTF-8.
- `README.md`: user-facing setup and run instructions.
- `temperature_experiment.py`: a small experiment that compares answers at different temperatures. It is not part of the classifier. Don't modify it unless asked.

## Setup and run

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-genai pydantic
export GEMINI_API_KEY="..."
python email_classifier.py   # run from the email-classifier/ folder
```

The script uses a relative path (`Path("emails")`), so it must run from the `email-classifier/` folder.

## Conventions

- The model name lives in the `MODEL` constant. Keep it in one place.
- Classification output is validated with the Pydantic `Classification` model through `response_schema`. Keep the categories in sync between the `Literal` type and the `RULES` prompt.
- Keep `temperature=0` for classification so results are consistent.
- Retry only on `errors.ServerError` (5xx). Do not retry `errors.ClientError` (4xx).
- Keep the prompt rules as they are unless asked to change them.
