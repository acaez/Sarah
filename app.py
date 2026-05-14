from flask import Flask, render_template, request, jsonify, Response
from ollama import chat

from config import CHAT_MODEL, FLASK_PORT, FLASK_DEBUG, SYSTEM_PROMPT
from core.memory import Memory
from core.conv import Conversation
from core.tts import synthesize

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")

memory = Memory()
conversation = Conversation()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat_route():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "message vide"}), 400

    try:
        contexte_memoire = memory.search(user_input)
    except Exception:
        contexte_memoire = ""

    system_content = SYSTEM_PROMPT + (
        f"\n\nSouvenirs de conversations précédentes :\n{contexte_memoire}"
        if contexte_memoire else ""
    )

    conversation.add("user", user_input)

    try:
        response = chat(
            model=CHAT_MODEL,
            messages=[{"role": "system", "content": system_content}] + conversation.get()
        )
        reply = response.message.content
    except Exception as e:
        conversation.pop_last()
        return jsonify({"error": str(e)}), 500

    conversation.add("assistant", reply)

    try:
        memory.store(user_input, reply)
    except Exception:
        pass

    return jsonify({"response": reply})


@app.route("/tts", methods=["POST"])
def tts_route():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "texte vide"}), 400
    audio = synthesize(text)
    return Response(audio, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT)
