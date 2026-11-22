# AGENTS.md

## Project

An agent that connects to a currency exchange MCP server (`https://currency-mcp.wesbos.com/mcp`), loads its tools, and asks a Gemini model to answer a currency question using them. The example prompt converts 100 USD to EUR with `convert_currency`.

## Layout

- `agent.py`: the agent. Connects to the MCP server, cleans the tool schemas, creates the model and agent, runs the example prompt, and prints the conversation.
- `requirements.txt`: dependencies.
- `README.md`: user-facing setup and run instructions.

## Conventions

- Keep the code small and readable.
- Don't commit or push unless asked.
