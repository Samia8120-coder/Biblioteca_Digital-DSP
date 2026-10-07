from collections import Counter
from typing import Any


def calcular_estatisticas(documentos: list[dict[str, Any]]) -> dict:
    total_documentos = len(documentos)
    espaco_utilizado_bytes = sum(d.get("tamanho", 0) for d in documentos)

    por_extensao = Counter(d["extensao"].lstrip(".") for d in documentos)
    por_categoria = Counter(d["categoria"] for d in documentos)
    por_autor = Counter(d["autor"] for d in documentos)

    return {
        "total_documentos": total_documentos,
        "espaco_utilizado_bytes": espaco_utilizado_bytes,
        "por_extensao": dict(por_extensao),
        "por_categoria": dict(por_categoria),
        "por_autor": dict(por_autor),
    }