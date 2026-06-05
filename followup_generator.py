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

def generate_followup(question, answer):

    prompt = f"""
You are CognitoScope.

Original Question:
{question}

User Answer:
{answer}

Generate ONE follow-up question that explores
the user's reasoning more deeply.

Return ONLY the question.
"""

    response = model.generate_content(
        prompt
    )

    return response.text