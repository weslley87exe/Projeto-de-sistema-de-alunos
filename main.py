# main.py
import os
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import crud
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "meubanco.db")

# Se seu crud aceita receber DB_PATH, exporte de lá ou defina a variável global — aqui assumimos que crud usa "meubanco.db" por padrão.
# Certifique-se que crud.criar_tabela() cria a tabela se necessário.
crud.criar_tabela()

app = FastAPI()

# Templates e static (garante que Render ache /templates e /static)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Rota web (index)
@app.get("/")
def index(request: Request, nome: str | None = None, matricula: str | None = None):
    alunos = crud.listar_alunos(nome, matricula)
    return templates.TemplateResponse("index.html", {"request": request, "alunos": alunos, "termo": nome or matricula or ""})

# Formulário adicionar (web)
@app.post("/adicionar")
def adicionar(nome: str = Form(...), idade: int = Form(...), nota: str = Form(...), matricula: str = Form(...)):
    from schemas import AlunoCreate
    aluno = AlunoCreate(nome=nome, idade=idade, nota=nota, matricula=matricula)
    novo_id = crud.adicionar_aluno(aluno)
    if novo_id is None:
        raise HTTPException(status_code=400, detail="Matrícula já existe")
    return RedirectResponse("/", status_code=303)

# Editar (web)
@app.post("/editar/{matricula_old}")
def editar(matricula_old: str, nome: str = Form(...), idade: int = Form(...), nota: str = Form(...), nova_matricula: str = Form(...)):
    from schemas import AlunoUpdate
    aluno = AlunoUpdate(nome=nome, idade=idade, nota=nota, matricula=nova_matricula)
    ok = crud.atualizar_aluno(matricula_old, aluno)
    if not ok:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return RedirectResponse("/", status_code=303)

# Deletar (web)
@app.post("/deletar/{matricula}")
def deletar(matricula: str):
    ok = crud.remover_aluno(matricula)
    if not ok:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return RedirectResponse("/", status_code=303)

# API simples REST (opcional, mantê-las se já tiver)
@app.get("/alunos")
def api_listar():
    return crud.listar_alunos()

@app.post("/alunos")
def api_adicionar(aluno: dict):
    # Se quiser, adapte pra pydantic aqui; eu deixei simples
    from schemas import AlunoCreate
    a = AlunoCreate(**aluno)
    novo_id = crud.adicionar_aluno(a)
    if novo_id is None:
        raise HTTPException(status_code=400, detail="Matrícula já existe")
    return {"id": novo_id}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # certo
    uvicorn.run(app, host="0.0.0.0", port=port)
