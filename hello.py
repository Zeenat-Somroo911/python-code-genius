import os
import chainlit as cl
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-2.0-flash")

# 👋 Welcome Message when app starts
@cl.on_chat_start
async def start():
    await cl.Message(content="""
👋 **Welcome to Python Code Explainer Bot!**

🧠 I can:
1. 📖 Explain your Python code line by line in English and Roman Urdu
2. 🐛 Highlight bugs or bad practices
3. 💡 Suggest better versions of your code

⚠️ *Please paste valid Python code only.*

Let's begin! 🚀
""").send()

# 📩 Main message handler
@cl.on_message
async def main(message: cl.Message):
    user_code = message.content.strip()

    # Check if it's likely Python code
    if not any(keyword in user_code for keyword in ["def", "print", "=", "import", "class", ":", "()"]):
        await cl.Message(content="⚠️ This bot only explains Python code. Please enter valid Python code.").send()
        return

    prompt = f"""
You are an expert Python developer who explains code to students.

Do the following:
1. Explain the code **line by line in English first**, then also explain the same line in **Roman Urdu**.
2. If there are any bugs, syntax errors, or bad practices, explain clearly in both English and Roman Urdu.
3. Suggest better or optimized code, and again explain the suggestions in English and Roman Urdu.

Code:
{user_code}
"""

    try:
        response = model.generate_content(prompt)
        await cl.Message(content=response.text).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
