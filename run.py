import json
from app.llm import generate
from app.image import generate_image
from app.audio import generate_audio

PROMPT = """
You are a strict JSON generator.

Create EXACTLY 3 scenes.

Rules:
- Always return 3 scenes
- Only robots (NO humans, NO children)
- Same robot in all scenes (yellow, small, round head)
- Keep prompts SHORT and VISUAL
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

def run():
    text = generate(PROMPT)
    print(text)

    data = json.loads(text)
    scenes = data["scenes"]

    for i, scene in enumerate(scenes, 1):
        generate_image(scene["image_prompt"], i)
        generate_audio(scene["description"], i)

    print("\nDone!")

if __name__ == "__main__":
    run()