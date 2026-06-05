import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Create model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_response(answer):

    prompt = f"""
You are CognitoScope, an expert reasoning analyst.

Analyze the user's response based on:

1. Clarity
2. Logic
3. Depth
4. Perspective Taking

Return ONLY in the following format:

Clarity: X/10
Logic: X/10
Depth: X/10
Perspective: X/10

Strengths:
- Point 1
- Point 2

Growth Areas:
- Point 1
- Point 2

Response:
{answer}
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"