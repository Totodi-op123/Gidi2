import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/HyperMoon/wav2vec2-base-960h-finetuned-deepfake"

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    payload = {"wait_for_model": True}
    # data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data, params={"wait_for_model": True})
    return json.loads(response.content.decode("utf-8"))

data = query("C:/Users/afrikaans1.mp3")
print(data)