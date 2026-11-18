from google.genai import types
from google import genai

client = genai.Client()  # takes the key from GEMINI_API_KEY

# prompt = "Complete the sentence with ONE word: The sky is..."
# prompt = """Complete the sentence "The sky is..." by choosing ONE single word that describes the state of the sky.

# Answer ONLY with one word, in lowercase, without periods or explanations."""

prompt = "Which city in France is on the edge of?"

for temp in [0, 1.5]:
    print(f"\n--- Temperature {temp} ---")
    for i in range(3):
        resp = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=temp),
        )
        print(resp.text.strip())

# --- Temperature 0 ---
# ...clear
# blue
# ...cloudy. (or "blue", "dark", "clear")

# --- Temperature 1.5 ---
# ...clear (or **blue**, **cloudy**, **gray**, etc.).

# Since you asked for **one word**, you can choose any of those, for example: **blue**.
# ...cloudy. (or "blue", "clear", etc.)

# Since you asked for just one word, let's pick: **blue** (or **cloudy**).
# cloudy (or clear, blue, gray, etc.)
