import hashlib
import os
import zipfile
from fastapi import APIRouter, HTTPException
from typing import List , Union
from http import HTTPStatus

from fastapi.responses import FileResponse
from models import Tutor
import csv

CSV_FILE_PATH = "tutores.csv"
ZIP_FILE_PATH = "tutores.zip"

router = APIRouter()

def load_tutores_from_csv() -> List[Tutor]:
    tutores = []
    try:
        with open("tutores.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tutores.append(Tutor(
                    id=row["id"],
                    nome=row["nome"],
                    email=row["email"],
                    login=row["login"],
                    senha=row["senha"],
                    nivel=row["nivel"],
                    turmas_ministradas=row["turmas"].split(", "),  # Separar por vírgula e espaço
                    tutores_responsavel=[int(x) for x in row["tutores_id"].split(",") if x.strip().isdigit()] if row["tutores_id"] else [],
                    idiomas_ministrados=row["idiomas"].split(", ")  # Separar por vírgula e espaço
                ))
    except FileNotFoundError:
        pass
    return tutores


def save_tutores_csv(tutores: List[Tutor]):
    """
    Salva um tutor no arquivo CSV
    """
    with open("tutores.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "nome", "email", "login", "senha", "nivel", "turmas", "tutores_id", "idiomas"])
        for tutor in tutores:
            writer.writerow([
                tutor.id, tutor.nome, tutor.email, tutor.login, tutor.senha,
                tutor.nivel, ", ".join(tutor.turmas_ministradas), 
                ", ".join(map(str, tutor.tutores_responsavel)) if tutor.tutores_responsavel else "",
                ", ".join(tutor.idiomas_ministrados)
            ])
#carrega o CSV de tutores
tutores = load_tutores_from_csv()


def count_entities_csv(file_path: str) -> int:
    """
    conta a quantidade de entidades de um CSV
    """
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            return sum(1 for row in reader)
    except FileNotFoundError:
        return 0

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


@router.post("/tutores/")
def create_tutor(tutor: Tutor):
    """
    criar e adicionar o novo tutor
    """
    if any(tutor_atual.id == tutor.id for tutor_atual in tutores):
        raise HTTPException(status_code=400, detail="ID já existente")
    tutores.append(tutor)
    save_tutores_csv(tutores)
    return tutor

@router.get("/tutores/")
def listar_tutores() -> List[Tutor]:
    return tutores


@router.put("/tutores/{tutor_id}")
def atualizar_tutor(tutor_id: int, tutor: Tutor):
    """
    Atualizar um tutor passando um ID
    """
    for i, tutor_atual in enumerate(tutores):
        if tutor_atual.id == tutor_id:
            tutores[i] = tutor
            save_tutores_csv(tutores)
            return tutor
    raise HTTPException(status_code=404, detail="Tutor não encontrado")


@router.delete("/tutores/{tutor_id}")
def excluir_tutor(tutor_id: int):
    """
    Deletar um tutor passando o ID
    """
    for i, tutor_atual in enumerate(tutores):
        if tutor_atual.id == tutor_id:
            del tutores[i]
            save_tutores_csv(tutores) 
            return {"message": "Tutor excluído com sucesso"}
    raise HTTPException(status_code=404, detail="Tutor não encontrado")


@router.get("/tutores/count")
def contar_tutores():
    """
    retornar a quantidade de tutores do arquivo CSV
    """
    return count_entities_csv("tutores.csv")


@router.post("/tutores/compactar_csv")
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

 
@router.get("/tutores/hash_csv")
def obter_hash_csv():
    """
    Retorna o hash SHA256 do arquivo CSV.
    """
    hash_csv = calcular_hash_sha256(CSV_FILE_PATH)
    return {"hash_sha256": hash_csv}