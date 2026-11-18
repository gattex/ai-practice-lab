# AI Practice Lab

A personal repository for studying artificial intelligence using real model APIs.

## Email classifier

`email_classifier.py` classifies support emails for an online sneaker store. It reads every `.txt` file in the `emails/` folder, sends each one to a Google Gemini model, and prints a category and a short summary.

It practices:

- System prompts (rules kept separate from each request)
- Structured output: the response is validated against a Pydantic model
- Temperature set to 0 for consistent answers
- Retries with exponential backoff when the server is busy (5xx), and no retries for client errors (4xx)

Categories: `Logistics`, `Finance`, `Sales`, `Exchanges and returns`, `Other`.

## Requirements

- Python 3.10 or higher
- A [Google AI Studio](https://aistudio.google.com/) API key

## Installation

From the repo root:

```bash
python3 -m venv venv
source venv/bin/activate

pip install google-genai pydantic
```

## API key setup

The SDK reads the key from an environment variable. Don't hardcode it in the code or commit it to the repo.

```bash
export GEMINI_API_KEY="your-gemini-key"
```

## Running

Run the script from the repo root, because it looks for the `emails/` folder using a relative path.

```bash
python email_classifier.py
```

### Trying your own emails

To add a case, create a new file in `emails/`, for example `emails/email_4.txt`, with the message text, and run the script again.

## Structure

```
ai-practice-lab/
├── email_classifier.py    # classification with structured output
└── emails/                # sample emails
```

## Notes

- Models change over time. If the model in `MODEL` stops being available, check the current Gemini model names in Google AI Studio and update the constant.
- This repo is for learning, not production code.
