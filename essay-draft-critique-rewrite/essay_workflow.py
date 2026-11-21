"""
Three-step essay workflow: draft, critique, rewrite.

Each step is a separate call to Gemini. The output of one step is the
input of the next one.

Usage (run from the essay-draft-critique-rewrite/ folder):
    python essay_workflow.py "Should cities invest in public transport?"

Requirements:
    pip install google-genai
    export GEMINI_API_KEY="your-key"
"""

import random
import sys

from google import genai
from google.genai import types

MODEL = "gemini-3.5-flash-lite"
TOPICS = [
    "Should cities invest in public transport?",
    "Should social media be regulated for teenagers?",
    "Is remote work good for productivity?",
    "Should college education be free?",
    "Do electric cars really help the environment?",
    "Should homework be banned in primary school?",
    "Is artificial intelligence a threat to jobs?",
    "Should governments tax sugary drinks?",
    "Is space exploration worth its cost?",
    "Should cities limit car traffic in the center?",
]

client = genai.Client()  # takes the key from GEMINI_API_KEY


def ask(prompt: str, temperature: float) -> str:
    """Sends one prompt to Gemini and returns the text of the answer."""
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    return resp.text.strip()


def draft(topic: str) -> str:
    """Step 1: write the first draft from the topic."""
    prompt = f"""
You are a professional writer.

Write a complete draft essay about the following topic:
{topic}

The essay should include:
- Clear Thesis Statement
- Logical Structure
- Strong Evidence and Examples
- Cohesion and Linking Words
- Appropriate Tone

Do not invent sources or citations.
Write in English.
Do not use more than 700 words
"""
    return ask(prompt, temperature=0)

def critique(essay: str) -> str:
    """Step 2: review the draft. Temperature 0 keeps the review consistent."""
    prompt = f"""
You are a professional writer reviewer.

Review the following essay draft and return feedback.
---
{essay}
---

The feedback should be:
- Critical but constructive
- Address issues such as structure, clarity, strength of argument, and writing style

The feedback should contain:
- Paragraph form

Do not rewrite the essay. Only give feedback.
Write in English.
"""
    return ask(prompt, temperature=0)


def rewrite(original_draft: str, reflection: str) -> str:
    """Step 3: rewrite the draft using the critique."""
    prompt = f"""
You are a professional writer.

Improve and fix the next essay:
--
{original_draft}
--
Taking into account the following feedback, which was provided by another reviewer:
--
{reflection}
--

The new essay should include:
- Clear Thesis Statement
- Logical Structure
- Strong Evidence and Examples
- Cohesion and Linking Words
- Appropriate Tone

Do not invent sources or citations.
Write in English.
Do not use more than 700 words
Return only the revised essay, without comments or explanations.
"""
    return ask(prompt, temperature=0)


def shorten_essay(essay: str, words: int, model: str = "openai:gpt-4o") -> str:
    prompt = f"""The following essay has {words} words.
The maximum allowed is 500 words.

Shorten it to 500 words or fewer, keeping the thesis, structure and main arguments.
Return only the shortened essay, without comments.

---
{essay}
---"""
    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0),
    )
    return resp.text.strip();


def ensure_length(essay: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        words = len(essay.split())
        print(f"Attempt {attempt + 1}: {words} words")

        if words <= 500:
            print("✅ Length OK")
            return essay

        essay = shorten_essay(essay, words)

    print(f"⚠️ Not fixed after {max_retries} attempts ({len(essay.split())} words)")
    return essay



def main():
    topic = " ".join(sys.argv[1:]) or random.choice(TOPICS)
    print(f"Topic: {topic}")

    first_draft = draft(topic)
    print("\n=== 1. DRAFT ===\n" + first_draft)

    review = critique(first_draft)
    print("\n=== 2. CRITIQUE ===\n" + review)

    final = rewrite(first_draft, review)
    final = ensure_length(final);
    print("\n=== 3. REWRITE ===\n" + final)
    
    


if __name__ == "__main__":
    main()
