# CLAUDE.md

Repo-wide rules for AI Practice Lab. These apply to every subproject in this repo. A subproject may add its own `CLAUDE.md` or `AGENTS.md` with more specific rules, but it must not weaken the rules below.

## Language

- All code, comments, identifiers, docstrings, and documentation are written in English.

## Secrets

- Never commit API keys, tokens, passwords, or `.env` files.
- Read secrets from environment variables, never hardcode them.
- If a secret shows up in a file you are about to commit, remove it from the commit and tell the user.
