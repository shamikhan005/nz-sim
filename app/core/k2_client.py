import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("K2_API_KEY")
URL = "https://api.k2think.ai/v1/chat/completions"


def call_k2(messages, max_tokens=500):
    payload = {
        "model": "MBZUAI-IFM/K2-Think-v2",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
