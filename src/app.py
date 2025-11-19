# src/app.py
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

# Carrega .env da raiz do projeto
load_dotenv()

# Tenta importar a nova interface OpenAI; se não, usa fallback antigo
try:
    from openai import OpenAI
    new_openai = True
except Exception:
    import openai
    new_openai = False

app = Flask(__name__)

# cria client conforme a versão instalada
if new_openai:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return render_template("index.html", error="Por favor escreva o contexto da mensagem.")

    user_message = (
        f"Crie uma mensagem profissional, curta e educada para a seguinte situação:\n\n{prompt}\n\n"
        "Inclua saudação, corpo objetivo e fechamento. Use um tom formal e claro."
    )

    try:
        # tenta nova interface
        if new_openai and hasattr(client, "chat") and hasattr(client.chat, "completions"):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=300,
                temperature=0.2
            )
            # extrai de formas robustas
            try:
                text = response.choices[0].message["content"].strip()
            except Exception:
                try:
                    text = response.choices[0].message.content.strip()
                except Exception:
                    text = str(response)
        else:
            # fallback para API antiga
            response = client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=300,
                temperature=0.2
            )
            text = response.choices[0].message.content.strip()

    except Exception as e:
        # Detecta problemas de cota ou erros e aplica fallback local se necessário
        err_text = str(e).lower()
        if "insufficient_quota" in err_text or "429" in err_text or "quota" in err_text:
            # fallback simples local (gera mensagem razoável sem IA)
            def local_fallback_generate(prompt_text):
                # montagem simples: saudação, frase com desculpa baseada no prompt, e fechamento
                lines = []
                lines.append("Olá,")
                # heurística para usar o prompt no corpo
                cleaned = prompt_text.strip()
                # se tem "atraso" ou "envio", usar frase específica
                if "atras" in cleaned.lower() or "atraso" in cleaned.lower() or "envio" in cleaned.lower():
                    lines.append(f"Peço desculpas pelo atraso no envio do documento referente a {cleaned}.")
                else:
                    # usa como motivo direto
                    lines.append(f"Peço desculpas pelo inconveniente. {cleaned.capitalize()}.")
                lines.append("")
                lines.append("Agradeço a compreensão.")
                lines.append("Atenciosamente,")
                lines.append("[Seu Nome]")
                return "\n".join(lines)

            text = local_fallback_generate(prompt)
            notice = ("(Resposta gerada localmente — API indisponível/sem cota. "
                      "Quando houver crédito a resposta será gerada pela IA.)\n\n")
            return render_template("index.html", prompt=prompt, result=notice + text)
        else:
            # outro erro: mostra mensagem amigável (útil para debug)
            return render_template("index.html", prompt=prompt, error=f"Erro ao chamar a API: {e}")

    return render_template("index.html", prompt=prompt, result=text)


if __name__ == "__main__":
    app.run(debug=True)
