import openai
from prompts import *
openai.api_base = "http://localhost:11434/v1/"
openai.api_key = "ollama"  # dummy key, required but ignored

client = openai.Client(
    base_url="http://localhost:11434/v1",
    api_key="key"
)
def get_ai_response(text):
    response = client.chat.completions.create(
        model="qwen3:1.7b",  # change to your model name
        temperature = 0.4,
        messages=[{
            'role': 'user',
            'content': prompt(text, think=False),
        }]
    )
    return response.choices[0].message.content