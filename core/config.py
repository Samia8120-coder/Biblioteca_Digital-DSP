from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve()
CONFIG_FILE = BASE_DIR/"config.yaml"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

DIRETORIO_DOCUMENTOS = BASE_DIR/config["storage"]["diretorio_documentos"]
DIRETORIO_METADADOS = BASE_DIR/config["storage"]["diretorio_matadados"]
DIRETORIO_BACKUPS = BASE_DIR/config["storage"]["diretorio_backups"]
DIRETORIO_EXPORTS = BASE_DIR/config["storage"]["diretorio_exports"]
ARQUIVOS_METADADOS = DIRETORIO_METADADOS/"documentos.json"

LOG_ARQUIVO = BASE_DIR/config["logging"]["arquivo"]
LOG_NIVEL = config["logging"]["nivel"]