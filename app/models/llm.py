from openai import OpenAI

class CallAPIOpenAI:
    def __init__(self, model_name, api_key):
        self.model_name = model_name
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def generate_content(self,prompt: list[dict[str,str]])->str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt
        )
        return response.choices[0].message.content