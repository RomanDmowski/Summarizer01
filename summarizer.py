# summarizer.py

import openai
import os
from openai import OpenAI

# Simple function to summarize text using OpenAI's GPT-3.5-turbo model.
# You can add more sophisticated prompt engineering if desired.

# Initialize the client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_text(text, client):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Please summarize the following text:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Failed to generate summary: {str(e)}")
