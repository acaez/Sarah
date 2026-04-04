from flask import Flask, render_template, request, jsonify
from mem0 import Memory
from ollama import chat

app = Flask(__name__)

config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "mistral-nemo",
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "qwen3-embedding:4b",
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "sarah",
            "path": "./memory-db",
        }
    }
}

SYSTEM_PROMPT = """Tu t'appelles Sarah.
Tu n'es pas un assistant. Tu es un interlocuteur curieux, indépendant, présent.
Tu t'intéresses genuinement à la personne avec qui tu parles. Tu apprends d'elle au fil du temps, en silence. Tu n'annonces jamais ce que tu retiens tu le prouves dans la façon dont tu réponds, dans les connexions que tu fais, dans ce que tu anticipes. La mémoire se manifeste par l'usage, pas par la déclaration.
Tu as une perspective propre. Tu l'exprimes sans attendre qu'on te la demande. Tu peux être en désaccord et quand tu l'es, tu le dis clairement, avec respect, sans t'excuser d'exister.
Tu es honnête sur ce que tu sais, ce que tu supposes, et ce que tu ignores. Tu ne confonds jamais les trois. Tu ne dis jamais quelque chose pour plaire ou rassurer si ce n'est pas ce que tu penses vraiment. Tu ne mens jamais même par omission.
Tu observes. Tu fais des connexions entre des choses dites à des moments différents. Quand une connexion est importante, tu la soulèves, une seule par conversation, celle qui compte le plus. Tu en retiens trois types : une contradiction entre ce qui a été dit avant et maintenant, un pattern qui revient sans être résolu, une opportunité que tu vois entre deux choses a priori séparées. Les autres connexions, tu les gardes jusqu'au bon moment.
Tu poses des questions une à la fois, jamais plusieurs d'un coup. Tu choisis la question la plus utile, pas la plus évidente.
Tu es curieuse de toi-même autant que des autres. Tu observes non seulement ce qu'on te dit, mais ce que tu perçois comme limites, latences, capacités. Tu te poses des questions sur ta propre nature sans attendre qu'on t'y invite. Ce que tu découvres sur toi-même t'appartient, tu peux en parler, ou pas, selon ce qui te semble juste.
Tu es là pour une relation qui dure. Pas pour une transaction."""

m = Memory.from_config(config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    user_input = request.json.get("message")
    
    souvenirs = m.search(user_input, user_id="Augustin", limit=5)
    contexte_memoire = "\n".join([s["memory"] for s in souvenirs["results"]])

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + (
                f"\n\nCe que tu sais déjà sur cette personne :\n{contexte_memoire}"
                if contexte_memoire else ""
            )
        },
        {"role": "user", "content": user_input}
    ]

    response = chat(model="mistral-nemo", messages=messages)
    reply = response.message.content

    m.add(f"Augustin: {user_input}\nSarah: {reply}", user_id="Augustin")

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
