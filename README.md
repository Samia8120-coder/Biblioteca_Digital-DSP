# Cofre Digital - Biblioteca Digital

Trabalho Prático 1 da disciplina QXD0099 - Desenvolvimento de Software para Persistência
Universidade Federal do Ceará, Campus Quixadá
Prof. Francisco Victor da Silva Pinheiro

## Integrantes

- [Ivna Leite]
- [Maria Grazyele]
- [Sâmia Feitosa]

## Tema

**Tema 15 - Biblioteca Digital**

O sistema armazena materiais bibliográficos digitais, como livros, artigos, apostilas, arquivos PDF, EPUB, TXT e imagens, junto com os metadados de cada material.

## Objetivo

Desenvolver, em Python com FastAPI, uma aplicação chamada Cofre Digital de Arquivos, capaz de armazenar, consultar, atualizar, excluir, proteger, exportar e fazer backup de arquivos digitais.

A persistência dos metadados é feita em arquivo JSON, sem uso de banco de dados. As configurações ficam em um arquivo YAML externo e as operações são registradas em um arquivo de log.

## Requisitos

- Python 3.10 ou superior
- pip
- Git (para clonar o repositório)

## Bibliotecas utilizadas

| Biblioteca | Para que serve |
|---|---|
| fastapi | Framework que cria a API e gera a documentação automática |
| uvicorn | Servidor que executa a API |
| pydantic | Modelos de dados e validação das entradas |
| pyyaml | Leitura dos arquivos de configuração `.yaml` |
| python-multipart | Recebimento de arquivos enviados pela API |

Também são usados módulos que já vêm com o Python: `json`, `hashlib`, `logging`, `zipfile`, `csv`, `mimetypes`, `pathlib` e `datetime`.

## Instruções de instalação

1. Clone o repositório e entre na pasta:

```powershell
git clone https://github.com/Samia8120-coder/Biblioteca_Digital-DSP.git
cd Biblioteca_Digital-DSP
```

2. Crie o ambiente virtual:

```powershell
python -m venv .venv
```

3. Ative o ambiente virtual:

```powershell
.venv\Scripts\activate
```

Se o PowerShell bloquear a execução de scripts, rode uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

4. Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Instruções de execução

Com o ambiente virtual ativado, na pasta raiz do projeto:

```powershell
uvicorn main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger), onde todas as rotas podem ser testadas, fica em:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

As pastas dentro de `storage/` são criadas automaticamente na primeira execução.

### Dados de demonstração

O repositório já acompanha documentos cadastrados em `storage/documentos/` e `storage/metadata/documentos.json`, com pelo menos 15 arquivos, 4 extensões e 3 categorias diferentes, incluindo arquivos de texto e binários. Assim, a API já inicia com dados.

Novos documentos podem ser enviados pelo `POST /documentos`, direto no Swagger (`/docs`), escolhendo o arquivo e preenchendo título, autor, ano e categoria.

## Estrutura do projeto

```
Biblioteca_Digital-DSP/
├── main.py                      ponto de entrada, registra as rotas
├── config.yaml                  configurações (pastas, log)
├── logging.yaml                 formato e destinos do log
├── requirements.txt             dependências
├── core/
│   ├── config.py                lê o config.yaml
│   └── logging_config.py        configura o logging a partir dos dois YAML
├── models/
│   └── documento.py             modelos Pydantic (Documento, DocumentoUpdate)
├── routes/
│   ├── documentos.py            CRUD, filtros, download, integridade, estatísticas
│   ├── integridade.py           verificação de integridade global
│   ├── exportar.py              exportação para CSV
│   └── backups.py               criação e listagem de backups
├── services/
│   ├── json_repository.py       leitura e escrita do documentos.json
│   ├── arquivo_service.py       salvar, apagar e calcular hash dos arquivos
│   ├── estatisticas_service.py  cálculo das estatísticas
│   ├── export_service.py        geração do CSV
│   └── backup_service.py        geração e listagem dos ZIPs
└── storage/                     criada automaticamente
    ├── documentos/              arquivos originais
    ├── metadata/                documentos.json
    ├── logs/                    sistema.log
    ├── backups/                 backups em ZIP
    └── exports/                 exportações
```

Cada camada tem uma responsabilidade: as rotas recebem as requisições, os serviços fazem o trabalho com arquivos e dados, e os modelos definem o formato dos documentos.

## Configuração

O arquivo `config.yaml` controla o comportamento do sistema:

```yaml
storage:
  diretorio_documentos: "./storage/documentos"
  diretorio_metadados: "./storage/metadata"
  diretorio_backups: "./storage/backups"
  diretorio_exports: "./storage/exports"

logging:
  arquivo: "./storage/logs/sistema.log"
  nivel: "INFO"
```

Alterar o `nivel` (por exemplo, para `WARNING` ou `DEBUG`) ou qualquer diretório e reiniciar a API muda o comportamento do sistema, sem editar código.

## Metadados dos documentos

Metadados gerais, gerados pelo sistema no momento do upload:

| Campo | Descrição |
|---|---|
| id | Identificador único, gerado automaticamente |
| nome_original | Nome do arquivo como foi enviado |
| nome_armazenado | Nome usado no armazenamento (`id_nomeoriginal`), evita sobrescrita |
| extensao | Extensão do arquivo (`.pdf`, `.epub`, `.txt`, ...) |
| tipo_mime | Tipo MIME identificado a partir do nome |
| tamanho | Tamanho em bytes |
| data_upload | Data e hora do envio |
| sha256 | Hash SHA-256 calculado no upload |
| categoria | Categoria ou gênero do material |
| descricao | Descrição opcional |

Metadados específicos da Biblioteca Digital, informados no upload:

| Campo | Descrição |
|---|---|
| titulo | Título do material |
| autor | Autor do material |
| ano | Ano de publicação |
| editora | Editora (opcional) |

Exemplo de registro salvo em `storage/metadata/documentos.json`:

```json
{
  "id": 1,
  "nome_original": "dom_casmurro.txt",
  "nome_armazenado": "1_dom_casmurro.txt",
  "extensao": ".txt",
  "tipo_mime": "text/plain",
  "tamanho": 15,
  "categoria": "romance",
  "descricao": null,
  "data_upload": "2026-10-07T22:55:41",
  "sha256": "5686fb2d5132d1dbfedf1f11c7487ae247105f88b89a36519bb860a4798f25bc",
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano": 1899,
  "editora": "Garnier"
}
```

## Principais endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/documentos` | Envia um arquivo com seus metadados |
| GET | `/documentos` | Lista os documentos, com filtros opcionais |
| GET | `/documentos/estatisticas` | Estatísticas do cofre |
| GET | `/documentos/{id}` | Consulta os metadados de um documento |
| GET | `/documentos/{id}/download` | Baixa o arquivo original |
| GET | `/documentos/{id}/integridade` | Confere se o arquivo foi alterado |
| PUT | `/documentos/{id}` | Atualiza metadados (parcial) |
| DELETE | `/documentos/{id}` | Remove o registro e o arquivo |
| GET | `/integridade` | Verifica a integridade de todos os documentos |
| GET | `/exportar/csv` | Exporta o catálogo em CSV |
| POST | `/backup` | Gera um backup compactado em ZIP |
| GET | `/backups` | Lista os backups existentes |

### Filtros de `GET /documentos`

| Parâmetro | Tipo | Comportamento |
|---|---|---|
| categoria | texto | Igual à categoria (ignora maiúsculas e minúsculas) |
| extensao | texto | Formato do arquivo, com ou sem ponto (`pdf` ou `.pdf`) |
| autor | texto | Contém o texto informado (`machado` encontra `Machado de Assis`) |
| ano | número | Ano de publicação exato |
| tamanho_min | número | Tamanho mínimo em bytes |
| tamanho_max | número | Tamanho máximo em bytes |

Os filtros podem ser combinados.

## Funcionalidade específica do tema: busca combinada

O requisito do tema 15 é permitir buscas combinando **autor**, **ano**, **categoria** e **formato do arquivo**. Isso é feito pelo `GET /documentos`, que lê os dados do `documentos.json` e aplica, em sequência, cada filtro informado. Só permanecem na resposta os documentos que atendem a todos os filtros ao mesmo tempo. Os filtros não informados são ignorados.

Exemplos:

```
GET /documentos?autor=machado
GET /documentos?autor=machado&ano=1899
GET /documentos?categoria=romance&extensao=epub
GET /documentos?autor=alencar&ano=1865&categoria=romance&extensao=pdf
```

A mesma lógica de filtro por autor e categoria também está disponível no backup seletivo (`POST /backup?categoria=romance`).

## Exemplos de utilização

Os exemplos usam `curl.exe` (no PowerShell, `curl` é um apelido de outro comando). Todos podem ser feitos também pelo Swagger em `/docs`.

Enviar um documento:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/documentos" -F "arquivo=@dom_casmurro.txt" -F "titulo=Dom Casmurro" -F "autor=Machado de Assis" -F "ano=1899" -F "categoria=romance" -F "editora=Garnier"
```

Listar com filtros combinados:

```powershell
curl.exe "http://127.0.0.1:8000/documentos?autor=machado&ano=1899&categoria=romance"
```

Atualizar apenas a editora:

```powershell
curl.exe -X PUT "http://127.0.0.1:8000/documentos/1" -H "Content-Type: application/json" -d "{\"editora\": \"Nova Editora\"}"
```

Baixar o arquivo original:

```powershell
curl.exe -o baixado.txt "http://127.0.0.1:8000/documentos/1/download"
```

Verificar a integridade de um documento:

```powershell
curl.exe "http://127.0.0.1:8000/documentos/1/integridade"
```

Resposta esperada:

```json
{
  "id": 1,
  "nome": "dom_casmurro.txt",
  "hash_original": "5686fb2d...",
  "hash_atual": "5686fb2d...",
  "integro": true
}
```

Se o arquivo em `storage/documentos/` for alterado manualmente, `hash_atual` muda e `integro` passa a ser `false`.

Estatísticas:

```powershell
curl.exe "http://127.0.0.1:8000/documentos/estatisticas"
```

```json
{
  "total_documentos": 15,
  "espaco_utilizado_bytes": 12348,
  "por_extensao": {"txt": 4, "epub": 4, "pdf": 5, "jpg": 2},
  "por_categoria": {"romance": 5, "tecnico": 5, "infantil": 3, "poesia": 2},
  "por_autor": {"Machado de Assis": 2, "José de Alencar": 2}
}
```

Gerar backup (geral e seletivo):

```powershell
curl.exe -X POST "http://127.0.0.1:8000/backup"
curl.exe -X POST "http://127.0.0.1:8000/backup?categoria=romance"
curl.exe "http://127.0.0.1:8000/backups"
```

## Decisões de projeto

- **Persistência:** os metadados ficam em `storage/metadata/documentos.json`. Toda operação lê e grava nesse arquivo, então os dados continuam disponíveis depois de reiniciar a API. A gravação é feita primeiro em um arquivo temporário e depois renomeada, para que o JSON não fique corrompido caso a gravação seja interrompida.
- **Nomes de arquivo:** o arquivo é salvo como `id_nomeoriginal`, o que impede que dois arquivos com o mesmo nome se sobrescrevam. O nome original é preservado nos metadados.
- **Integridade:** o hash SHA-256 é calculado no upload, lendo o arquivo em blocos, e recalculado nas verificações de integridade.
- **Exclusão:** `DELETE /documentos/{id}` remove o registro do JSON e também o arquivo físico em `storage/documentos/`.
- **Atualização:** `PUT /documentos/{id}` altera somente os campos enviados e nunca mexe no arquivo físico, no hash, no tamanho ou no nome armazenado.
- **Backup:** o ZIP contém o `documentos.json` e os arquivos físicos. O nome inclui data e hora (`backup_AAAA-MM-DD_HHMMSS.zip`) e, se o nome já existir, recebe um sufixo numérico, então um backup nunca sobrescreve outro.
- **Log:** as operações são registradas em `storage/logs/sistema.log` com data, hora, nível e informações da operação. Falhas de integridade e tentativas de acessar documentos inexistentes são registradas como `WARNING`, e arquivos físicos ausentes como `ERROR`.
- **Erros:** documento inexistente retorna 404, dados inválidos retornam 422, e arquivo físico ausente retorna 404.