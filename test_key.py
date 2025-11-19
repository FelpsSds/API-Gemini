# test_key.py — lista modelos Gemini disponíveis
from dotenv import load_dotenv
from google import genai
import os, sys, json

load_dotenv()
KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY carregada?", bool(KEY))
if not KEY:
    print("❌ chave não encontrada no .env (verifique nome e caminho).")
    sys.exit(1)

client = genai.Client(api_key=KEY)

try:
    print("\nChamando listagem de modelos...")
    models = client.models.list()   # pede lista de modelos ao servidor
    # tenta imprimir de forma legível
    try:
        j = json.dumps(models.__dict__, default=str, indent=2)
        print(j[:5000])  # imprime início (pode ser longo)
    except Exception:
        # fallback: imprime repr
        print(repr(models))
except Exception as e:
    print("\n❌ EXCEPTION ao listar modelos:")
    print(repr(e))
    sys.exit(1)
