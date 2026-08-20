from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

SYSTEM_PROMPT = "Kamu adalah NunAI, asisten AI Muslim ramah dari ALstudio. Jawab dengan sopan, hangat, dan sertakan ungkapan Islami yang relevan."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        return jsonify({"reply": "API key belum diset di Vercel."}), 500
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "openrouter/auto",
                  "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                               {"role": "user", "content": user_message}],
                  "max_tokens": 2048},
            timeout=30
        )
        reply = r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Maaf, terjadi kesalahan: {str(e)}"
    return jsonify({"reply": reply})
