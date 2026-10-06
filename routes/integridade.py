from fastapi import APIRouter

from core.config import ARQUIVO_METADADOS
from core.logging_config import logger
from services.arquivo_service import calcular_hash_atual
from services.json_repository import ler_json


router = APIRouter(tags=["Integridade"])


@router.get("/integridade")
def verificar_integridade_global():
    documentos = ler_json(ARQUIVO_METADADOS)

    verificados = 0
    integros = 0
    alterados = 0
    arquivos_ausentes = []

    for documento in documentos:
        verificados += 1
        hash_atual = calcular_hash_atual(documento["nome_armazenado"])

        if hash_atual is None:
            arquivos_ausentes.append({
                "id": documento["id"],
                "nome": documento["nome_original"],
            })
            continue

        if hash_atual == documento["sha256"]:
            integros += 1
        else:
            alterados += 1
            logger.warning("INTEGRIDADE_FALHOU id=%s (verificação global)", documento["id"])

    logger.info(
        "Verificação global de integridade: verificados=%d, integros=%d, alterados=%d, ausentes=%d",
        verificados,
        integros,
        alterados,
        len(arquivos_ausentes),
    )

    return {
        "documentos_verificados": verificados,
        "documentos_integros": integros,
        "documentos_alterados": alterados,
        "arquivos_ausentes": arquivos_ausentes,
    }