import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv


load_dotenv()

CURRENCY_MCP_STREAMABLE = "https://currency-mcp.wesbos.com/mcp"  # recommended


def to_text(content):
    """Message content can be a string or a list of blocks. Return only the text."""
    if isinstance(content, str):
        return content

    parts = []
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block["text"])
    return "\n".join(parts)


def clean_schema(schema):
    """Remove JSON schema keys that Gemini does not support."""
    if isinstance(schema, dict):
        return {
            key: clean_schema(value)
            for key, value in schema.items()
            if key not in ("$schema", "additionalProperties")
        }
    if isinstance(schema, list):
        return [clean_schema(item) for item in schema]
    return schema


def print_chat(result):
    for m in result["messages"]:
        role = m.__class__.__name__

        if role == "HumanMessage":
            print(f"\n🧑 USER:\n{to_text(m.content)}")

        elif role == "AIMessage":
            print(f"\n🤖 ASSISTANT:\n{to_text(m.content)}")

        elif role == "ToolMessage":
            print(f"\n🛠️ TOOL ({m.name}):")
            print(to_text(m.content))


async def main():
    # 1) Connect to the MCP client
    client = MultiServerMCPClient(
        {
            "currency": {
                "transport": "streamable_http",
                "url": CURRENCY_MCP_STREAMABLE,
            }
        }
    )

    # 2) Fetch the tools from the MCP so the agent can use them
    tools = await client.get_tools()
    for tool in tools:
        if isinstance(tool.args_schema, dict):
            tool.args_schema = clean_schema(tool.args_schema)
    print("\n=== Available MCP tools ===")
    for tool in tools:
        print(f"- {tool.name}")

    model = init_chat_model(
        model="gemini-3.5-flash-lite",
        model_provider="google_genai",
        verbose=True)

    agent = create_agent(
        model=model,
        tools=tools
    )

    user_prompt = (
        "Convert 100 USD to EUR. "
        "Return only the numeric result and the currency code, e.g. '92.34 EUR'."
    )
    #     🤖 ASSISTANT:
    # [{'id': 'toolu_01GLsv2Nnppdi9Nmxzb6bt9s', 'input': {'amount': 100, 'from': 'USD', 'to': 'EUR'}, 'name': 'convert_currency', 'type': 'tool_use'}]

    # 🛠️ TOOL (convert_currency):
    # {"amount":1,"base":"USD","date":"2026-01-09","rates":{"EUR":0.85896},"conversion":{"from":"USD","to":"EUR","amount":100,"result":85.9,"rate":0.85896}}

    # 🤖 ASSISTANT:
    # The result of converting 100 USD to EUR is 85.9 EUR.

    # user_prompt = [
    #     {"role": "user", "content": "Give me the support currencies available in the currency MCP."}
    # ]
    # 🛠️ TOOL (get_currencies):
    # {"AUD":"Australian Dollar",
    # "BRL":"Brazilian Real",
    # "CAD":"Canadian Dollar",
    # "CHF":"Swiss Franc",
    # "CNY":"Chinese Renminbi Yuan",
    # "CZK":"Czech Koruna",
    # "DKK":"Danish Krone",
    # "EUR":"Euro","GBP":
    # "British Pound","HKD":"Hong Kong Dollar","HUF":"Hungarian Forint","IDR":"Indonesian Rupiah","ILS":"Israeli New Shekel","INR":"Indian Rupee","ISK":"Icelandic Króna","JPY":"Japanese Yen","KRW":"South Korean Won","MXN":"Mexican Peso","MYR":"Malaysian Ringgit","NOK":"Norwegian Krone","NZD":"New Zealand Dollar","PHP":"Philippine Peso","PLN":"Polish Złoty","RON":"Romanian Leu","SEK":"Swedish Krona","SGD":"Singapore Dollar","THB":"Thai Baht","TRY":"Turkish Lira","USD":"United States Dollar","ZAR":"South African Rand"}

    result = await agent.ainvoke({"messages": [{"role": "user", "content": user_prompt}]})

    last_msg = result["messages"][-1]

    print_chat(result)


if __name__ == "__main__":
    asyncio.run(main())
