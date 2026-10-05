import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

from core.config import DIRETORIO_DOCUMENTOS
from core.logging_config import logger

TAMANHO_BLOCO = 8192

def salvar_arquivo(arquivo: UploadFile, documento_id: int) -> dict:
    DIRETORIO_DOCUMENTOS.mkdir(parents=True, exist_ok=True)

    nome_original = arquivo.filename
    extensao = Path(nome_original).suffix
    nome_armazenado = f"{documento_id}_{nome_original}"
    caminho_destino = DIRETORIO_DOCUMENTOS/nome_armazenado

    hash_sha256 = hashlib.sha256()
    tamaho = 0

    with open(caminho_destino, "wb") as destino:
        while True:
            pedaco = arquivo.file.read(TAMANHO_BLOCO)
            if not pedaco:
                break
            destino.write(pedaco)
            hash_sha256.update(pedaco)
            tamanho += len(pedaco)

    tipo_mime, _ = mimetypes.guess_type(nome_original)

    logger.info(
        "Arquivo salvo: id=%s, nome_armazenado=%s, tamanho=%d",
        documento_id,
        nome_armazenado,
        tamaho,
    )

    return {
        "nome_original": nome_original,
        "nome_armazenado": nome_armazenado,
        "extensao": extensao,
        "tipo_mime": tipo_mime,
        "tamanho": tamanho,
        "sha256": hash_sha256.hexdigest(),
        "data_upload": datetime.now().isoformat(timespec="seconds"),
    }

def calcular_hash_atual(nome_armazenado: str) -> str | None:
    caminho = DIRETORIO_DOCUMENTOS/nome_armazenado

    if not caminho.exists():
        return None

    hash_sha256 = hashlib.sha256()

    with open(caminho, "rb") as file:
        while True:
            pedaco = file.read(TAMANHO_BLOCO)
            if not pedaco:
                break
            hash_sha256.update(pedaco)

    return hash_sha256.hexdigest()

def remover_arquivo(nome_armazenado: str) -> bool:
    caminho = DIRETORIO_DOCUMENTOS

    if not caminho.exists():
        return False

    caminho.unlike()
    return True

def caminho_do_arquivo(nome_armazenado: str) -> Path:
    return DIRETORIO_DOCUMENTOS/nome_armazenado