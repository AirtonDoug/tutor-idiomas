from pydantic import BaseModel

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

class Tutor(BaseModel):
    id: int
    nome: str
    email: str
    login: str
    senha: str
    nivel: str
    turmas_responsavel: list[str] = []
    alunos_id: list[int] = []
    idiomas: list[str] = []
