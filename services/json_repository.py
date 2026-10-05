import json
from pathlib import Path
from typing import Any

from core.logging_config import logger

def garantir_arquivo(arquivo: Path) -> None:
    arquivo.parent.mkdir(parents=True, exist_ok=True)

    if not arquivo.exists():
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

        logger.info("Arquivo JSON criado: %s", arquivo.name)

def ler_json(arquivo: Path) -> list[dict[str, Any]]:
    garantir_arquivo(arquivo)

    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as erro:
        logger.error("JSON inválido em %s: %s", arquivo.name, erro)
        raise ValueError(
            f"O arquivo {arquivo.name} contém JSON inválido."
        ) from erro

def escrever_json(arquivo: Path, dados: list[dict[str, Any]]) -> None:
    garantir_arquivo(arquivo)

    arquivo_temporario = arquivo.with_suffix(".tmp")
    with open(arquivo_temporario, "w", encoding="utf-8") as file:
        json.dump(dados, file, ensure_ascii=False, indent=4)

    arquivo_temporario.replace(arquivo)

    logger.debug(
        "Arquivo %s atualizando com %d registros.",
        arquivo.name,
        len(dados),
    )

def buscar_por_id(arquivo: Path, registro_id: int) -> dict[str, Any] | None:
    dados = ler_json(arquivo)

    for item in dados:
        if item["id"] == registro_id:
            return item

    return None

def proximo_id(arquivo:Path) -> int:
    dados = ler_json(arquivo)

    if not dados:
        return 1
    return max(item["id"] for item in dados) + 1

def adicionar(arquivo: Path, novo_registro: dict[str, Any]) -> None:
    dados = ler_json(arquivo)
    dados.append(novo_registro)
    escrever_json(arquivo, dados)

def atualizar(
    arquivo: Path,
    registro_id: int,
    campos_novos: dict[str, Any],
) -> dict[str, Any] | None:
    dados = ler_json(arquivo)

    for indice, item in enumerate(dados):
        if item["id"] == registro_id:
            item_atualizado = {**item, **campos_novos}
            dados[indice] = item_atualizado
            escrever_json(arquivo, dados)
            return item_atualizado

    return None

def remover(arquivo: Path, registro_id: int) -> dict[str, Any] | None:
    dados = ler_json(arquivo)

    removido = None
    nova_lista = []

    for item in dados:
        if item["id"] == registro_id:
            removido = item
        else:
            nova_lista.append(item)

    if removido is None:
        return None

    escrever_json(arquivo, nova_lista)
    return removido