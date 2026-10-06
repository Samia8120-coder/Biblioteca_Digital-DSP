from fastapi import APIRouter, HTTPException, status

from core.config import ARQUIVO_METADADOS
from core.logging_config import logger
from services.backup_service import criar_backup, listar_backups
from services.json_repository import ler_json


router = APIRouter(tags=["Backup"])


@router.post("/backup", status_code=status.HTTP_201_CREATED)
def criar_backup_geral(autor: str | None = None, categoria: str | None = None):
    documentos = ler_json(ARQUIVO_METADADOS)

    if autor:
        documentos = [d for d in documentos if autor.lower() in d["autor"].lower()]

    if categoria:
        documentos = [d for d in documentos if d["categoria"].lower() == categoria.lower()]

    if not documentos:
        logger.warning("Tentativa de backup sem documentos correspondentes aos filtros.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum documento encontrado para os filtros informados.",
        )

    caminho_backup = criar_backup(documentos)

    return {
        "mensagem": "Backup criado com sucesso.",
        "arquivo": caminho_backup.name,
        "quantidade_documentos": len(documentos),
    }


@router.get("/backups")
def listar_backups_disponiveis():
    backups = listar_backups()

    logger.info("Listagem de backups: %d encontrado(s).", len(backups))

    return backups