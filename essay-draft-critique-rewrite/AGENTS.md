# AGENTS.md

## Project

A three-step workflow with Google Gemini: the model writes an essay draft, critiques it, and rewrites it. The main file is `essay_workflow.py`.

## Layout

- `essay_workflow.py`: the workflow. Three functions (`draft`, `critique`, `rewrite`) and a `main()` that runs them in order.
- `README.md`: user-facing setup and run instructions.

## Conventions

- The model name lives in the `MODEL` constant. Keep it in one place.
- Each step builds its prompt inside its function (`draft`, `critique`, `rewrite`). Keep the prompt text as written unless asked to change it.
- Keep `temperature=0` for every step so results are consistent.
