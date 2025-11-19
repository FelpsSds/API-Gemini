# Gerador de Mensagens Profissionais

Pequena web app (Flask) que gera mensagens profissionais curtas a partir de um contexto. Suporta chamadas para OpenAI **(gpt-3.5 / gpt-5)** ou para **Gemini** (Google) e contém um fallback local caso a API esteja sem cota.

## Funcionalidades
- Gerar mensagem profissional (saudação + corpo objetivo + fechamento) a partir de um texto de contexto.
- Suporta OpenAI ou Gemini (conforme chave e SDK configurados).
- Fallback local quando API indisponível ou sem crédito.
- Projeto pensado para ser usado em Windows (VS Code + venv), mas funciona em Linux/macOS.

## Estrutura do projeto
Criador-de-mensagens-profissionais/
├─ .env # NÃO commitar (local com sua API key)
├─ .env.example # Exemplo das variáveis de ambiente (commitar)
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ src/
│ ├─ app.py
│ └─ templates/
│ └─ index.html
└─ .venv/ # ambiente virtual


## Tecnologias
- Python 3.12
- Flask 3.x
- python-dotenv
- openai (quando for usar OpenAI)
- google-genai (quando for usar Gemini)

## Setup (Windows) — passo a passo
1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO

## Crie e ative o ambiente virtual:

python -m venv .venv
# ativar no PowerShell
.venv\Scripts\Activate.ps1
# ou no cmd:
.venv\Scripts\activate.bat

## Instale as dependências:

pip install -r requirements.txt

##Crie o arquivo .env (local, NÃO commitar) ou copie o .env.example e preencha:

# exemplos de variáveis
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
FLASK_ENV=development

## Rodar a aplicação

$env:FLASK_APP="src.app"
$env:FLASK_ENV="development"
python -m flask run
# abre http://127.0.0.1:5000

Variáveis de ambiente (no .env local)

OPENAI_API_KEY — chave da OpenAI (se usar OpenAI)

GEMINI_API_KEY — chave do Google Gemini (se usar Gemini)

FLASK_ENV — environment (development/production)

Comportamento de fallback

Se a API responder com erro de cota (ou estiver indisponível), a aplicação gera uma mensagem local simples e informa que foi gerada localmente.

Segurança / Boas práticas

NUNCA commite chaves reais (.env) no repositório público.

Adicione .env ao .gitignore.

Se você acidentalmente comitou uma chave pública, gere uma nova chave no painel (rotate) imediatamente. Depois remova a chave do histórico do Git (veja seção abaixo).

Remover .env do repositório (se foi commited)
# remover do controle (mas manter local)
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env and add to .gitignore"
git push origin main


Se a chave foi publicada no histórico remoto (push), gere/rotacione a chave urgente no painel do provedor e use ferramentas como git filter-repo ou BFG repo-cleaner para limpar o histórico (veja abaixo).

Se precisa remover chaves do histórico remoto (avançado)

Opções:

usar BFG Repo-Cleaner (fácil) — https://rtyley.github.io/bfg-repo-cleaner/

usar git filter-repo (mais controlado)

Depois de limpar, forçar push:

git push --force origin main


Atenção: forçar push altera histórico — combine com a equipe.

Contribuições

Pull requests são bem-vindas. Antes de abrir PR, rode pip install -r requirements.txt e teste localmente.

Licença

Escolha uma licença (MIT, Apache-2.0, etc.). Ex.: MIT.


---

# 2) `.gitignore` sugerido

Crie (ou atualize) `.gitignore` na raiz com esse conteúdo:


Python

pycache/
*.py[cod]
*.pyo
*.pyd
*.pytest_cache/

venv

.venv/
venv/
env/

dotenv

.env
key.env
*.env

editor / OS

.vscode/
.idea/
.DS_Store
Thumbs.db

byte compiled

*.egg-info/
dist/
build/


---

# 3) `.env.example`

Crie ` .env.example` (commitável) com:


Copie este arquivo para .env e preencha suas chaves
NÃO COMMITAR o arquivo .env com chaves reais

OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development


---

# 4) Comandos Git práticos (ordem recomendada)

Supondo que você ainda não comitou `.env` (ou já removeu dele):

```bash
# 1) garantir que .env está ignorado e só .env.example está commited
echo ".env" >> .gitignore
git add .gitignore .env.example README.md
git commit -m "Add README, .gitignore and .env.example"
git push origin main


Se .env já foi comitado e você ainda não removeu do histórico remoto:

# remove do índice (mantém arquivo local)
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Remove .env from repo and add to .gitignore"
git push origin main


Se a chave já vazou em commits antigos (já deu push com chave pública) — passos recomendados:

Rotacione a chave no painel do provedor (OpenAI/GCP) — gere uma nova e apague a antiga.

Limpe o histórico com BFG ou git filter-repo:

BFG (exemplo):

# instalar BFG (java)
bfg --delete-files .env
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force


git filter-repo é outra opção (recomendo ler docs).

Peça aos colaboradores para fazerem git fetch e git reset --hard origin/main localmente após você forçar o push.

Importante: quando houver vazamento de chave sempre rotacione (revoke) a chave no painel do provedor antes de tentar limpar historico.
