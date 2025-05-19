import openai
from config import gemini_key
from prompts import *
from google import genai

def get_ai_response(text):
    return gemini_response(text)

def openai_response(text):
    client = openai.Client(
        base_url="http://localhost:11434/v1",
        api_key="key"
    )
    response = client.chat.completions.create(
        model="qwen3:1.7b",  # change to your model name
        temperature = 0.4,
        messages=[{
            'role': 'user',
            'content': prompt(text, think=False),
        }]
    )
    return response.choices[0].message.content
def gemini_response(text):
    client = genai.Client(api_key=gemini_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", 
        contents=prompt(text, think=True)
        )
    return response.text