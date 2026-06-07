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

def generate_profile(answers):

    combined_answers = "\n\n".join(answers)

    prompt = f"""
You are CognitoScope.

Analyze all responses below.

Create a final cognitive profile.

Evaluate:

1. Logic
2. Depth
3. Perspective Taking
4. Clarity

Return ONLY:

Reasoning Style:
(creative title)

Logic: X/10
Depth: X/10
Perspective: X/10
Clarity: X/10

Strengths:
- Point 1
- Point 2

Growth Areas:
- Point 1
- Point 2

Responses:
{combined_answers}
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Profile generation unavailable: {str(e)}"