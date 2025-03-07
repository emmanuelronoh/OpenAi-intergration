import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to GPT-3.5 Turbo
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
