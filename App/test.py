import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Use a model you actually have access to
model = genai.GenerativeModel("models/gemini-2.0-pro-exp-02-05")

response = model.generate_content("Say hi like a friendly robot.")
print(response.text)
