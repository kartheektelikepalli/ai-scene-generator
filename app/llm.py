import requests
from .config import OLLAMA_URL, MODEL

def generate(prompt: str) -> str:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 1000   # 🔥 VERY IMPORTANT
            }
        }
    )
    return res.json()["response"]