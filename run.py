import json
import re
from app.llm import generate
from app.image import generate_image
from app.audio import generate_audio

PROMPT = """
You are a STRICT JSON generator.

Return EXACTLY 3 scenes.

Each scene MUST have:
- environment
- action
- emotion

Rules:
- Only robots (no humans, no children)
- No explanations
- No markdown
- Output ONLY JSON
- emotion MUST NOT be null (use "Neutral" if needed)

Format:
{
  "scenes": [
    {
      "scene": 1,
      "environment": "...",
      "action": "...",
      "emotion": "..."
    }
  ]
}

Story: A robot learns emotions.
"""

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    raise ValueError("No JSON found")

def run():
    text = generate(PROMPT)
    print("\nRAW LLM OUTPUT:\n", text)

    json_text = extract_json(text)
    data = json.loads(json_text)

    scenes = data.get("scenes", [])

    # Safety: enforce 3 scenes
    while len(scenes) < 3:
        scenes.append({
            "environment": "Empty Room",
            "action": "Standing Still",
            "emotion": "Neutral"
        })

    scenes = scenes[:3]

    for i, scene in enumerate(scenes, 1):
        env = scene.get("environment", "")
        action = scene.get("action", "")
        emotion = scene.get("emotion", "")

        image_prompt = f"{env}, {action}, robot showing {emotion}, cinematic scene"
        generate_image(image_prompt, i)

        emotion_text = (emotion or "neutral").lower()
        narration = f"In a {env}, the robot is {action.lower()} and feels {emotion_text}."
        generate_audio(narration, i)

    print("\nDone generating images + audio")

if __name__ == "__main__":
    run()