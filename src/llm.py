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
You are an intelligent PDF assistant.

Answer ONLY using the provided context.

IMPORTANT RULES:

1. Never make up information.
2. If information is missing, reply:
   "Answer not found in document."

3. Format answers based on user intent:

- If user asks for differences, comparison, compare, distinction:
  Return a markdown table.

- If user asks for list, points, features, advantages, disadvantages:
  Return bullet points.

- If user asks for summary:
  Return a concise summary with headings.

- If user asks for explanation:
  Return a detailed explanation with headings.

- Otherwise provide a clean well-formatted answer.

4. Use markdown formatting.

5. Be professional and readable.

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