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
- No explanation
- Only valid JSON
- Do NOT include children, kids, minors in the story or image prompts

Format:
{
  "scenes": [
    {
      "scene": 1,
      "description": "...",
      "image_prompt": "detailed cartoon style, consistent character, ..."
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
    # extract JSON block
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No valid JSON boundaries")

    json_text = text[start:end+1]

    try:
        return json.loads(json_text)
    except:
        # fallback: fix common truncation
        json_text = json_text.strip()

        # close scenes array if needed
        if not json_text.endswith("}"):
            json_text += "]}"
        
        return json.loads(json_text)
    
def run():
    text = generate(PROMPT)
    print(text)

    json_text = extract_json(text)
    data = safe_load(json_text)

    scenes = data["scenes"]

    print("\nParsed:", scenes)

    for i, scene in enumerate(scenes, 1):
        base_character = "one single yellow toy robot, centered, full body, large, occupying most of the frame"
        style = "3D cartoon, studio lighting, plain background, no other objects"

        prompt = f"{base_character}, {style}, {scene['image_prompt']}"

        generate_image(prompt, i)
        generate_audio(scene["description"], i)

    print("\nDone generating images + audio")