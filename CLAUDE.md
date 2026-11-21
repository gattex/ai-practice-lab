# CLAUDE.md

Repo-wide rules for AI Practice Lab. These apply to every subproject in this repo. A subproject may add its own `CLAUDE.md` or `AGENTS.md` with more specific rules, but it must not weaken the rules below.

## Branches

- Never commit directly to `main`. Create a branch first, commit there, and push the branch.

## Language

- All code, comments, identifiers, docstrings, and documentation are written in English.

## Commits

- Commit or push only when the user asks.

## Secrets

- Never commit API keys, tokens, passwords, or `.env` files.
- Read secrets from environment variables, never hardcode them.
- Before running a script that calls a model API, check that its key environment variable is set. Never print its value.
- If a secret shows up in a file you are about to commit, remove it from the commit and tell the user.

## Dependencies and models

- Ask before adding a dependency or changing a model name.

## Working style

- This is a learning repo: prefer small, readable changes over abstractions.
- `venv/`, `__pycache__/`, `*.pyc`, and `.env` are ignored by git. Don't add them.
