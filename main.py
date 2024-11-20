import hashlib
import os
import zipfile
from fastapi import FastAPI, HTTPException
from typing import List , Union
from http import HTTPStatus

from fastapi.responses import FileResponse
from models import Aluno
import csv

CSV_FILE_PATH = "alunos.csv"
ZIP_FILE_PATH = "alunos.zip"

app = FastAPI()


# Carregar dados do arquivo CSV

def load_alunos_from_csv() -> List[Aluno]:
    alunos = []
    try:
        with open("alunos.csv",mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                alunos.append(Aluno(
                    id=int(row["id"]),
                    nome=row["nome"],
                    email=row["email"],
                    login=row["login"],
                    senha=row["senha"],
                    nivel=row["nivel"],
                    turma_participante=row["turma_participante"],
                    tutor_responsavel=row["tutor_responsavel"],
                    aulas_assistidas=int(row["aulas_assistidas"])
                ))
    except FileNotFoundError:
        pass
    return alunos

# Salvar alunos no CSV

def save_alunos_csv(alunos:List[Aluno]):
    with open("alunos.csv",mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "nome", "email", "login", "senha", "nivel", "turma_participante", "tutor_responsavel", "aulas_assistidas"])
        for aluno in alunos:
            writer.writerow([
                aluno.id, aluno.nome, aluno.email, aluno.login, aluno.senha,
                aluno.nivel, aluno.turma_participante, aluno.tutor_responsavel,
                aluno.aulas_assistidas
            ])

# carregar alunos do csv
alunos = load_alunos_from_csv()

# Contar entidades no csv

def count_entities_csv(file_path: str) -> int:
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            return sum(1 for row in reader)
    except FileNotFoundError:
        return 0
#Função para calcular o hash sha256
def calcular_hash_sha256(file_path: str) -> str:
    """
    Calcula o hash SHA256 de um arquivo.
    """
    try:
        with open(file_path, "rb") as file:
            sha256 = hashlib.sha256()
            while chunk := file.read(8192):  # Lê o arquivo em blocos de 8KB
                sha256.update(chunk)
            return sha256.hexdigest()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")

# Create Aluno
@app.post("/alunos/")
def create_aluno(aluno: Aluno):
    if any(aluno_atual.id == aluno.id for aluno_atual in alunos):
        raise HTTPException(status_code=400, detail="ID já existe")
    alunos.append(aluno)
    save_alunos_csv(alunos)
    return aluno


# Read Alunos

@app.get("/alunos/")
def listar_alunos() -> List[Aluno]:
    return alunos

# Update Aluno

@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, aluno: Aluno):
    for i, aluno_atual in enumerate(alunos):
        if aluno_atual.id == aluno_id:
            alunos[i] = aluno
            save_alunos_csv(alunos)
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

# Delete Aluno

@app.delete("/alunos/{aluno_id}")
def excluir_aluno(aluno_id: int, aluno: Aluno):
    for i, aluno_atual in enumerate(alunos):
        if aluno_atual.id == aluno_id:
            del alunos[i]
            save_alunos_csv(alunos)
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

# Count Alunos

@app.get("/alunos/count")
def contar_alunos():
    return count_entities_csv("alunos.csv")

@app.post("/compactar_csv/")
def compactar_csv():
    """
    Compacta o arquivo CSV em um arquivo ZIP e o retorna.
    """
    # Verifica se o arquivo CSV existe
    if not os.path.exists(CSV_FILE_PATH):
        return {"error": "Arquivo CSV não encontrado"}

    # Cria o arquivo ZIP
    with zipfile.ZipFile(ZIP_FILE_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(CSV_FILE_PATH, arcname=os.path.basename(CSV_FILE_PATH))

    # Retorna o arquivo ZIP
    return FileResponse(
        ZIP_FILE_PATH,
        media_type="application/zip",
        filename=os.path.basename(ZIP_FILE_PATH)
    )

#endpoint que retorna o hash sha256 de um arquivo CSV  
@app.get("/hash_csv/")
def obter_hash_csv():
    """
    Retorna o hash SHA256 do arquivo CSV.
    """
    hash_csv = calcular_hash_sha256(CSV_FILE_PATH)
    return {"hash_sha256": hash_csv}