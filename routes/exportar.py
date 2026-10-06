from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from core.config import ARQUIVO_METADADOS
from core.logging_config import logger
from services.export_service import gerar_csv_em_memoria
from services.json_repository import ler_json


router = APIRouter(prefix="/exportar", tags=["Exportação"])


@router.get("/csv")
def exportar_csv():
    documentos = ler_json(ARQUIVO_METADADOS)

    conteudo_csv = gerar_csv_em_memoria(documentos)

    logger.info("Exportação CSV solicitada: %d documento(s).", len(documentos))

    return StreamingResponse(
        iter([conteudo_csv]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=documentos.csv"},
    )