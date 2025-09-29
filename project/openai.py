import os
import time
import json
import requests
from dotenv import load_dotenv
from collections import defaultdict

class ChatgptMetrics:
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.latencies = []
        self.status_codes = defaultdict(int)

    def log(self, status_code, latency):
        self.total_calls += 1
        self.latencies.append(latency)
        self.status_codes[status_code] += 1
        if status_code == 200:
            self.successful_calls += 1
        else:
            self.failed_calls += 1

    def print_summary(self):
        print("\n--- ChatGPT API Metrics ---")
        print(f"Total Calls: {self.total_calls}")
        print(f"Successful Calls: {self.successful_calls}")
        print(f"Failed Calls: {self.failed_calls}")
        if self.latencies:
            print(f"Avg Latency: {sum(self.latencies)/len(self.latencies):.2f} sec")
        print(f"Status Codes: {dict(self.status_codes)}")


class Chatgpt:
    metrics = ChatgptMetrics()  # shared metrics for all instances

    def __init__(self, prompt, parameter, user_parameter,key):
        load_dotenv(".env")
        self.key = key
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.key} ",
            "Content-Type": "application/json"
        }

        self.prompt = prompt

        if parameter == "A":
            self.body = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": self.prompt}],
                "temperature": 0.7
            }
        elif parameter == "B":
            self.para = user_parameter
            self.body = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": self.prompt},
                    {"role": "user", "content": self.para}
                ],
                "temperature": 0.7
            }


        start_time = time.time()
        self.connection = requests.post(
            url=self.url,
            headers=self.headers,
            data=json.dumps(self.body)
        )
        latency = time.time() - start_time


        Chatgpt.metrics.log(self.connection.status_code, latency)

        if self.connection.status_code != 200:
            print(f"ERROR {self.connection.status_code} \n {self.connection.json()}")

    def get_response(self):
        if self.connection.status_code == 200:
            outcome = self.connection.json()
            output = outcome["choices"][0]["message"]["content"]
            print(output)
            return output
        return None
