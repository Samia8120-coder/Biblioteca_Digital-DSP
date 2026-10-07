from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from core.config import ARQUIVO_METADADOS
from core.logging_config import logger
from models.documento import Documento, DocumentoUpdate
from services.arquivo_service import (
    calcular_hash_atual,
    caminho_do_arquivo,
    remover_arquivo,
    salvar_arquivo,
)
from services.estatisticas_service import calcular_estatisticas
from services.json_repository import (
    adicionar,
    atualizar,
    buscar_por_id,
    ler_json,
    proximo_id,
    remover,
)


router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"],
)


@router.post("", response_model=Documento, status_code=status.HTTP_201_CREATED)
def criar_documento(
    arquivo: UploadFile = File(...),
    titulo: str = Form(...),
    autor: str = Form(...),
    ano: int = Form(...),
    categoria: str = Form(...),
    editora: str | None = Form(None),
    descricao: str | None = Form(None),
):
    documento_id = proximo_id(ARQUIVO_METADADOS)

    info_arquivo = salvar_arquivo(arquivo, documento_id)

    dados = {
        "id": documento_id,
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "categoria": categoria,
        "editora": editora,
        "descricao": descricao,
        **info_arquivo,
    }

    adicionar(ARQUIVO_METADADOS, dados)

    logger.info("Documento cadastrado: id=%s, titulo=%s", documento_id, titulo)

    return dados


@router.get("", response_model=list[Documento])
def listar_documentos(
    categoria: str | None = None,
    extensao: str | None = None,
    autor: str | None = None,
    ano: int | None = None,
    tamanho_min: int | None = None,
    tamanho_max: int | None = None,
):
    documentos = ler_json(ARQUIVO_METADADOS)

    if categoria:
        documentos = [d for d in documentos if d["categoria"].lower() == categoria.lower()]

    if extensao:
        extensao_normalizada = extensao if extensao.startswith(".") else f".{extensao}"
        documentos = [d for d in documentos if d["extensao"].lower() == extensao_normalizada.lower()]

    if autor:
        documentos = [d for d in documentos if autor.lower() in d["autor"].lower()]

    if ano:
        documentos = [d for d in documentos if d["ano"] == ano]

    if tamanho_min is not None:
        documentos = [d for d in documentos if d["tamanho"] >= tamanho_min]

    if tamanho_max is not None:
        documentos = [d for d in documentos if d["tamanho"] <= tamanho_max]

    logger.info("Listagem de documentos: %d registro(s).", len(documentos))

    return documentos


@router.get("/estatisticas")
def estatisticas_documentos():
    # precisa vir antes de /{documento_id}, senão o FastAPI tenta tratar
    # "estatisticas" como se fosse um id
    documentos = ler_json(ARQUIVO_METADADOS)

    resultado = calcular_estatisticas(documentos)

    logger.info("Estatísticas calculadas: %d documento(s).", resultado["total_documentos"])

    return resultado


@router.get("/{documento_id}", response_model=Documento)
def obter_documento(documento_id: int):
    documento = buscar_por_id(ARQUIVO_METADADOS, documento_id)

    if not documento:
        logger.warning("Documento não encontrado: %s", documento_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    return documento


@router.get("/{documento_id}/download")
def baixar_documento(documento_id: int):
    documento = buscar_por_id(ARQUIVO_METADADOS, documento_id)

    if not documento:
        logger.warning("Download de documento inexistente: %s", documento_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    caminho = caminho_do_arquivo(documento["nome_armazenado"])

    if not caminho.exists():
        logger.error("Arquivo físico ausente: id=%s, caminho=%s", documento_id, caminho)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo físico não encontrado.")

    logger.info("Download: id=%s, arquivo=%s", documento_id, documento["nome_original"])

    return FileResponse(
        path=caminho,
        filename=documento["nome_original"],
        media_type=documento.get("tipo_mime") or "application/octet-stream",
    )


@router.get("/{documento_id}/integridade")
def verificar_integridade(documento_id: int):
    documento = buscar_por_id(ARQUIVO_METADADOS, documento_id)

    if not documento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    hash_atual = calcular_hash_atual(documento["nome_armazenado"])

    if hash_atual is None:
        logger.error("Verificação de integridade: arquivo físico ausente. id=%s", documento_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Arquivo físico não encontrado.")

    integro = hash_atual == documento["sha256"]

    if not integro:
        logger.warning("INTEGRIDADE_FALHOU id=%s", documento_id)
    else:
        logger.info("Integridade verificada: id=%s, integro=%s", documento_id, integro)

    return {
        "id": documento_id,
        "nome": documento["nome_original"],
        "hash_original": documento["sha256"],
        "hash_atual": hash_atual,
        "integro": integro,
    }


@router.put("/{documento_id}", response_model=Documento)
def atualizar_documento(documento_id: int, dados: DocumentoUpdate):
    campos_novos = dados.model_dump(exclude_unset=True)

    documento_atualizado = atualizar(ARQUIVO_METADADOS, documento_id, campos_novos)

    if documento_atualizado is None:
        logger.warning("Tentativa de atualizar documento inexistente: %s", documento_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    logger.info("Documento atualizado: %s", documento_id)

    return documento_atualizado


@router.delete("/{documento_id}")
def excluir_documento(documento_id: int):
    removido = remover(ARQUIVO_METADADOS, documento_id)

    if removido is None:
        logger.warning("Tentativa de remover documento inexistente: %s", documento_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento não encontrado.")

    remover_arquivo(removido["nome_armazenado"])

    logger.info("Documento removido: %s", documento_id)

    return {"mensagem": "Documento removido com sucesso."}