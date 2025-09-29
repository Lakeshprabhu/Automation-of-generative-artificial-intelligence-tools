import os
import time
from dotenv import load_dotenv
from google import genai
from collections import defaultdict


class GeminiMetrics:
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.latencies = []
        self.fail_reasons = defaultdict(int)

    def log(self, success, latency=None, error=None):
        self.total_calls += 1
        if success:
            self.successful_calls += 1
            self.latencies.append(latency)
        else:
            self.failed_calls += 1
            self.fail_reasons[str(error)] += 1

    def print_summary(self):
        print("\n--- Gemini API Metrics ---")
        print(f"Total Calls: {self.total_calls}")
        print(f"Successful Calls: {self.successful_calls}")
        print(f"Failed Calls: {self.failed_calls}")
        if self.latencies:
            print(f"Avg Latency: {sum(self.latencies)/len(self.latencies):.2f} sec")
        if self.fail_reasons:
            print(f"Failure Reasons: {dict(self.fail_reasons)}")


class Gemini:
    metrics = GeminiMetrics()

    def __init__(self,key):
        load_dotenv(".env")
        self.api = key
        self.gemini_connection = genai.Client(api_key=self.api)

    def gen(self, prompt, user_content):
        try:
            start_time = time.time()

            if user_content is None:
                self.response = self.gemini_connection.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            else:
                self.response = self.gemini_connection.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[user_content, "\n\n", prompt]
                )

            latency = time.time() - start_time
            Gemini.metrics.log(success=True, latency=latency)

        except Exception as e:
            Gemini.metrics.log(success=False, error=e)
            print(f"ERROR: {e}")
            self.response = None

    def get_response(self):
        if not self.response:
            return None

        try:
            source = self.response.candidates[0].content
            source = list(source)
            source_2 = [i for i in source][0]
            readable_source = [x for x in source_2]
            unpacked_source = readable_source[1]

            answer = "".join(pain.text for pain in unpacked_source)
            return answer

        except Exception as e:
            print(f"ERROR while extracting response: {e}")
            return None
