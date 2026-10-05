import logging
import logging.config
from pathlib import Path

import yaml

from core.config import LOG_ARQUIVO, LOG_NIVEL


BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING_FILE = BASE_DIR / "logging.yaml"

with open(LOGGING_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

LOG_ARQUIVO.parent.mkdir(parents=True, exist_ok=True)

config["handlers"]["file"]["filename"] = str(LOG_ARQUIVO)
config["loggers"]["cofre_digital"]["level"] = LOG_NIVEL

logging.config.dictConfig(config)

logger = logging.getLogger("cofre_digital")
logger.info("Sistema de logging inicializado.")