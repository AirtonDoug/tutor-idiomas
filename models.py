from typing import List, Optional
from pydantic import BaseModel
from typing import List, Optional

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
    turmas_ministradas: List[str]
    tutores_responsavel: Optional[List[int]] = None
    idiomas_ministrados: List[str]
