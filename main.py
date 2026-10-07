from fastapi import FastAPI

from routes.backups import router as backups_router
from routes.documentos import router as documentos_router
from routes.exportar import router as exportar_router
from routes.integridade import router as integridade_router
from core.logging_config import logger


app = FastAPI(
    title="Cofre Digital - Biblioteca Digital",
    description="Sistema de armazenamento e gerenciamento de documentos da biblioteca digital.",
    version="0.3.0",
)

app.include_router(documentos_router)
app.include_router(integridade_router)
app.include_router(exportar_router)
app.include_router(backups_router)


@app.get("/", tags=["Sistema"])
def home():
    logger.info("Endpoint raiz acessado.")

    return {
        "mensagem": "Cofre Digital - Biblioteca Digital",
        "recursos": [
            "/documentos",
            "/documentos/estatisticas",
            "/integridade",
            "/exportar/csv",
            "/backup",
            "/backups",
            "/docs",
            "/redoc",
        ],
    }