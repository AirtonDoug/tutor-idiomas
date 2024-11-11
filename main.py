from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List , Union
from http import HTTPStatus


app = FastAPI()

class Aluno(BaseModel):
    id: int
    nome: str
    email: str
    login: str
    senha: str
    nivel: str
    turma_participante: str
    tutor_responsavel: str
    aulas_assistidas: int

alunos: List[Aluno] = []

# Create Aluno
@app.post("/alunos/")
def create_aluno(aluno: Aluno):
    if any(aluno_atual.id == aluno.id for aluno_atual in alunos):
        raise HTTPException(status_code=400, detail="ID já existe")
    alunos.append(aluno)
    return aluno


# Read Alunos

@app.get("/alunos/", response_model=List[Aluno])
def listar_alunos():
    return alunos

# Update Alunos

@app.put("/alunos/{aluno_id}",response_model=Aluno)
def atualizar_aluno(aluno_id: int, aluno: Aluno):
    for i, aluno_atual in enumerate(alunos):
        if aluno_atual.id == aluno_id:
            alunos[i] = aluno
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

# Delete Alunos

@app.delete("/alunos/{aluno_id}",response_model=Aluno)
def excluir_aluno(aluno_id: int, aluno: Aluno):
    for i, aluno_atual in enumerate(alunos):
        if aluno_atual.id == aluno_id:
            del alunos[i]
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")