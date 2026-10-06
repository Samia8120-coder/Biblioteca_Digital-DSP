import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from core.config import ARQUIVO_METADADOS, DIRETORIO_BACKUPS
from core.logging_config import logger
from services.arquivo_service import caminho_do_arquivo


def criar_backup(documentos: list[dict[str, Any]]) -> Path:
    """
    Cria um arquivo ZIP com os arquivos físicos listados em `documentos` e o
    documentos.json. Usa data e hora no nome para nunca sobrescrever um backup
    anterior.
    """
    DIRETORIO_BACKUPS.mkdir(parents=True, exist_ok=True)

    agora = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    nome_backup = f"backup_{agora}.zip"
    caminho_backup = DIRETORIO_BACKUPS / nome_backup

    # Garante que o nome nunca é reaproveitado, mesmo em testes muito rápidos.
    contador = 1
    while caminho_backup.exists():
        nome_backup = f"backup_{agora}_{contador}.zip"
        caminho_backup = DIRETORIO_BACKUPS / nome_backup
        contador += 1

    with zipfile.ZipFile(caminho_backup, "w", zipfile.ZIP_DEFLATED) as zip_arquivo:
        if ARQUIVO_METADADOS.exists():
            zip_arquivo.write(ARQUIVO_METADADOS, arcname="documentos.json")

        for documento in documentos:
            caminho_arquivo = caminho_do_arquivo(documento["nome_armazenado"])

            if caminho_arquivo.exists():
                zip_arquivo.write(caminho_arquivo, arcname=f"documentos/{documento['nome_armazenado']}")
            else:
                logger.warning(
                    "Backup: arquivo físico ausente, pulado. id=%s, arquivo=%s",
                    documento["id"],
                    documento["nome_armazenado"],
                )

    logger.info("Backup criado: %s (%d documento(s))", nome_backup, len(documentos))

    return caminho_backup


def listar_backups() -> list[dict[str, Any]]:
    """Lista os backups existentes, com nome e tamanho em bytes."""
    DIRETORIO_BACKUPS.mkdir(parents=True, exist_ok=True)

    backups = []

    for caminho in sorted(DIRETORIO_BACKUPS.glob("*.zip")):
        backups.append({
            "arquivo": caminho.name,
            "tamanho": caminho.stat().st_size,
        })

    return backups