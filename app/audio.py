from gtts import gTTS
import os

def generate_audio(text: str, idx: int):
    os.makedirs("output/audio", exist_ok=True)

    path = f"output/audio/scene_{idx}.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(path)

    print(f"Saved: {path}")