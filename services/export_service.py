import csv
import io
from datetime import datetime
from pathlib import Path
from typing import Any

from core.config import DIRETORIO_EXPORTS
from core.logging_config import logger


CAMPOS_CSV = [
    "id",
    "nome_original",
    "extensao",
    "categoria",
    "tamanho",
    "data_upload",
    "sha256",
    "titulo",
    "autor",
    "ano",
    "editora",
]


def gerar_csv(documentos: list[dict[str, Any]]) -> Path:
    """Gera um arquivo CSV com o catálogo de documentos e devolve o caminho dele."""
    DIRETORIO_EXPORTS.mkdir(parents=True, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H%M")
    caminho = DIRETORIO_EXPORTS / f"documentos_{agora}.csv"

    with open(caminho, "w", encoding="utf-8", newline="") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=CAMPOS_CSV, extrasaction="ignore")
        escritor.writeheader()

        for documento in documentos:
            escritor.writerow(documento)

    logger.info("Exportação CSV gerada: %s (%d registro(s))", caminho.name, len(documentos))

    return caminho


def gerar_csv_em_memoria(documentos: list[dict[str, Any]]) -> str:
    """Gera o CSV como texto, sem salvar em disco (usado para a resposta HTTP)."""
    buffer = io.StringIO()
    escritor = csv.DictWriter(buffer, fieldnames=CAMPOS_CSV, extrasaction="ignore")
    escritor.writeheader()

    for documento in documentos:
        escritor.writerow(documento)

    return buffer.getvalue()