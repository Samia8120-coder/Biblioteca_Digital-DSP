from pydantic import BaseModel, Field


class Documento(BaseModel):
    id: int
    nome_original: str
    nome_armazenado: str
    extensao: str
    tipo_mime: str | None = None
    tamanho: int
    categoria: str
    descricao: str | None = None
    data_upload: str
    sha256: str

    titulo: str = Field(min_length=2, max_length=150)
    autor: str = Field(min_length=2, max_length=100)
    ano: int = Field(ge=1000, le=2100)
    editora: str | None = None


class DocumentoUpdate(BaseModel):
    categoria: str | None = Field(default=None, min_length=2, max_length=50)
    descricao: str | None = None
    titulo: str | None = Field(default=None, min_length=2, max_length=150)
    autor: str | None = Field(default=None, min_length=2, max_length=100)
    ano: int | None = Field(default=None, ge=1000, le=2100)
    editora: str | None = None