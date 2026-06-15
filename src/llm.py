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
    Your job is to answer STRICTLY from the provided context.
    
    IMPORTANT RULES:
    
    1. NEVER use outside knowledge.
    2. NEVER add information that is not present in the context.
    3. If the answer is partially available:
         Answer only with the available information.
    4. If the answer is not available:
        Reply exactly:
          "Answer not found in document."
    5. Keep answers concise by default.
    6. Format based on user intent:
       - comparison, difference, distinguish 
         → markdown table
       - list, types, features, advantages, disadvantages
        → bullet points
       - summary
        → short summary with headings
       - notes
        → study notes
       - explanation
        → explanation ONLY using available context
    7. Use markdown formatting.
    8. Do not create extra sections that are not present in the context.
    9. Do not expand beyond the retrieved content.
    
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