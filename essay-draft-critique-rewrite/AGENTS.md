# AGENTS.md

## Project

A three-step workflow with Google Gemini: the model writes an essay draft, critiques it, and rewrites it. The main file is `essay_workflow.py`.

## Layout

- `essay_workflow.py`: the workflow. Three functions (`draft`, `critique`, `rewrite`) and a `main()` that runs them in order.
- `README.md`: user-facing setup and run instructions.

## Conventions

- The API key comes from the `GEMINI_API_KEY` environment variable. Never hardcode keys or commit `.env` files.
- The model name lives in the `MODEL` constant. Keep it in one place.
- Each step builds its prompt inside its function (`draft`, `critique`, `rewrite`). Keep the prompt text as written unless asked to change it.
- Keep `temperature=0` for every step so results are consistent.
- All code, comments, docs, and prompts are in English.

## Working in this repo

- It's a learning repo: prefer small, readable changes over abstractions.
- There is no test suite or `requirements.txt` yet. If you add one, say so in the summary.
- Don't commit or push unless asked.
- `venv/` and `__pycache__/` are ignored by git. Don't add them.
