from gtts import gTTS
import os

def generate_audio(text: str, idx: int):
    os.makedirs("output/audio", exist_ok=True)

    tts = gTTS(text=text, lang="en")
    path = f"output/audio/scene_{idx}.mp3"
    tts.save(path)

    print(f"Saved: {path}")