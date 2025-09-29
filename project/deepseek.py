import os

import requests
from dotenv import load_dotenv


class Deepseek():
    def __init__(self,prompt,file,key):
        load_dotenv(".env")

        self.api_key =key
        self.url="https://api.deepseek.com/v1/chat/completions"
        self.headers = {'Authorization':f"Bearer {self.api_key}",
                        'Content-Type':'application/json'}

        prompt+=f"File below:- \n\n{file} "

        self.data={"model":"deepseek-chat",
                   "messages":[{"role":"user","content":prompt}],
                    "temperature":0.7,
                    "max_tokens":150}

        self.connection = requests.post(url=self.url,headers=self.headers,json=self.data)

        if self.connection.status_code == 200:
            outcome = self.connection.json()
            self.response_content = outcome["choices"][0]["message"]["content"]
            print(outcome["choices"][0]["message"]["content"])

        else:
            print(f"Error {self.connection.status_code}")


    def get_response(self):
        return self.response_content

