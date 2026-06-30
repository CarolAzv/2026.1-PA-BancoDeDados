from fastapi import FastAPI
from app.routers import veiculos

app = FastAPI(
    title="API de Veículos",
    description="API construída na disciplina de PABD - TADS/IFRN",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"mensagem": "API de Veículos no ar!"}