from openai import OpenAI
from openai import OpenAI
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt

class AI:
    def __init__(self):
        self.GPT_MODEL = "gpt-4o"
        self.api = os.environ.get("openai_key")
        self.client = OpenAI(api_key=self.api)

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(self,messages, tools=None, tool_choice=None, model=None):
        if model is None:
            model = self.GPT_MODEL
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice=tool_choice,
            )
            return response
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e