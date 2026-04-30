import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def generate(prompt: str) -> str:
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 800
            }
        }
    )

    return res.json()["response"]