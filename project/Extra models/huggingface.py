import os

import requests
from dotenv import load_dotenv

class Hugging():
    def __init__(self):
        load_dotenv("../.env")

        self.url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
        self.headers ={"Authorization":f"Bearer {os.getenv('hugging_key')}",
                       "Content-Type":"application/json",
                       "x-use-cache": "false"}

        self.prompt = {"inputs":"What is AI"}

        self.response = requests.post(url = self.url,headers=self.headers,json=self.prompt)

        if self.response.status_code == 200:
            outcome = self.response.json()
            print(outcome)
        else:
            print(self.response.status_code)
            print(self.response.json)