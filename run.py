import json
import re
from app.llm import generate
from app.image import generate_image
from app.audio import generate_audio

PROMPT = """
You are a strict JSON generator.

Create EXACTLY 3 scenes.

Rules:
- Always return 3 scenes
- Never leave image_prompt empty
- Keep prompts SHORT (max 20 words)
- No explanation
- Only valid JSON

Format:
{
  "scenes": [
    {
      "scene": 1,
      "description": "...",
      "image_prompt": "..."
    }
  ]
}

Story: A robot learns emotions.
"""

def extract_json(text: str):
    match = re.search(r"\{.*", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No JSON found")

def safe_load(text: str):
    start = text.find("{")
    end = text.rfind("}")

    json_text = text[start:end+1]
    return json.loads(json_text)

def run():
    text = generate(PROMPT)
    print(text)

    json_text = extract_json(text)
    data = safe_load(json_text)

    scenes = data["scenes"]

    print("\nParsed:", scenes)

    for i, scene in enumerate(scenes, 1):
        generate_image(scene["image_prompt"], i)
        generate_audio(scene["description"], i)

    print("\nDone generating images + audio")

if __name__ == "__main__":
    run()