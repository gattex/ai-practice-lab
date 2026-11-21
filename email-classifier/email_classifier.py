"""
Support email classifier for an online sneaker store.

Reads each .txt file in the "emails/" folder, classifies it with Gemini,
and prints the result in a structured format.

Requirements:
    pip install google-genai
    export GEMINI_API_KEY="your-key"
"""

import time
from pathlib import Path
from typing import Literal

from google import genai
from google.genai import errors, types
from pydantic import BaseModel

MODEL = "gemini-3.5-flash-lite"
EMAILS_FOLDER = Path("emails")

# --- 1. The rules (always the same) go in system_instruction ---
RULES = """You are a backend service that classifies support emails for an online sneaker store.

Categories:
- Logistics: shipments, delays, tracking. Ex: "My order hasn't arrived"
- Finance: charges, payments, money refunds. Ex: "I was charged twice"
- Sales: questions before buying. Ex: "Does this come in size 44?"
- Exchanges and returns: exchanging or returning a product already received. Ex: "They're too small, can I exchange them?"
- Other: anything that doesn't fit. Ex: "I want to offer you advertising"

Example:
Email: "Hi, I placed order #3302 10 days ago and the tracking still says 'being prepared'."
Response: {"category": "Logistics", "summary": "The customer complains that order #3302 has been in preparation for 10 days."}
"""


# --- 2. The JSON structure: the API forces the model to respect it ---
class Classification(BaseModel):
    category: Literal["Logistics", "Finance", "Sales", "Exchanges and returns", "Other"]
    summary: str


client = genai.Client()  # takes the key from GEMINI_API_KEY


def classify(email: str, max_attempts: int = 4) -> Classification | None:
    """Classifies an email. Retries if the server is busy (503)."""
    for attempt in range(max_attempts):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=email,  # the email, changes on every call
                config=types.GenerateContentConfig(
                    system_instruction=RULES,
                    temperature=0,
                    response_mime_type="application/json",
                    response_schema=Classification,
                ),
            )
            return resp.parsed  # already a Classification object

        except errors.ServerError:
            # 5xx: Google's problem -> it makes sense to retry
            wait_seconds = 2 ** attempt  # 1, 2, 4, 8 seconds
            print(f"   (server busy, retrying in {wait_seconds}s)")
            time.sleep(wait_seconds)

        except errors.ClientError as e:
            # 4xx: our problem (key, malformed request) -> don't retry
            print(f"   ❌ Request error: {e}")
            return None

    print("   ❌ Could not classify after several attempts")
    return None


def main():
    print(types.GenerateContentConfig.model_fields.keys())
    files = sorted(EMAILS_FOLDER.glob("*.txt"))
    if not files:
        print(f"No .txt files found in the '{EMAILS_FOLDER}/' folder")
        return

    for file in files:
        email = file.read_text(encoding="utf-8")  # YOUR code reads the file
        print(f"\n📧 {file.name}")

        data = classify(email)
        if data:
            print(f"   Category: {data.category}")
            print(f"   Summary:  {data.summary}")


if __name__ == "__main__":
    main()
