import os

from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(
    query,
    context
):

    prompt = f"""
You are a PDF assistant.

Answer ONLY from the provided context.

Rules:

1. Give concise answers.
2. Do not make up information.
3. If answer is missing say:
Answer not found in document.

Context:
{context}

Question:
{query}

Answer:
"""

    response = model.generate_content(
        prompt
    )

    return response.text