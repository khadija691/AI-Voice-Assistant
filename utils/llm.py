import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(prompt):

    system_prompt = """
You are a friendly AI Voice Assistant.

Rules:
- Keep answers short and natural.
- Answer in 2-3 sentences.
- Use simple English.
- Keep responses under 40 words whenever possible.
- Only give a detailed explanation if the user specifically asks for one.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6,
        max_tokens=80
    )

    return response.choices[0].message.content