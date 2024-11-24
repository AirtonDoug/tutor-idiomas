from fastapi import FastAPI
from routes.aluno import router as aluno_router
from routes.tutor import router as tutor_router

app = FastAPI()

# Inclui os roteadores para os endpoints de Aluno e Tutor
app.include_router(aluno_router)
app.include_router(tutor_router)
