# src/app.py
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from google import genai   # SDK nova do Gemini

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

# cria o client Gemini
client = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt", "").strip()

    if not prompt:
        return render_template("index.html", error="Por favor escreva o contexto.")

    user_message = (
        "Crie uma mensagem profissional, clara e educada para a seguinte situação:\n\n"
        f"{prompt}\n\n"
        "Inclua saudação, corpo objetivo e fechamento."
    )

    try:
        # chamada real ao Gemini
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=user_message,
        )

        text = response.text

    except Exception as e:
        # fallback local
        fallback = (
            "(Resposta gerada localmente — integração Gemini não configurada.)\n\n"
            "Olá,\n"
            f"Peço desculpas pelo inconveniente. {prompt}.\n\n"
            "Agradeço a compreensão.\n"
            "Atenciosamente,\n"
            "[Seu Nome]"
        )
        return render_template("index.html", prompt=prompt, result=fallback)

    return render_template("index.html", prompt=prompt, result=text)


if __name__ == "__main__":
    app.run(debug=True)
