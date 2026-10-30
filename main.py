import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# Initialize the AI client using the environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def hello():
    return "Agent is running!"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/run-agent", methods=["POST", "GET"])
def run_agent():
    # Get the prompt from the request, or use a default one
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "Write a short, one-sentence motivational quote for a developer.")

    try:
        # Call the free Groq API (using Llama 3)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        response_text = completion.choices[0].message.content
        return jsonify({"status": "success", "response": response_text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))