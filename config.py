"""
config.py
---------

Configurações centralizadas do Portfolio Agent.
"""

from __future__ import annotations

import os

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


###############################################################################
# Configurações
###############################################################################

@dataclass(frozen=True)
class Config:

    #
    # Gemini
    #

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    #
    # Telegram
    #

    TELEGRAM_TOKEN = os.getenv(
        "TELEGRAM_TOKEN"
    )

    TELEGRAM_CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID"
    )

    TELEGRAM_PARSE_MODE = "Markdown"

    #
    # Email
    #

    EMAIL_USER = os.getenv(
        "EMAIL_USER"
    )

    EMAIL_PASS = os.getenv(
        "EMAIL_PASS"
    )

    EMAIL_DESTINO = os.getenv(
        "EMAIL_DESTINO"
    )

    SMTP_SERVER = os.getenv(
        "SMTP_SERVER",
        "smtp.gmail.com"
    )

    SMTP_PORT = int(
        os.getenv(
            "SMTP_PORT",
            587
        )
    )

    #
    # Sistema
    #

    CACHE_DIAS = int(
        os.getenv(
            "CACHE_DIAS",
            180
        )
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    TIMEOUT_HTTP = int(
        os.getenv(
            "TIMEOUT_HTTP",
            30
        )
    )

    #
    # Diretórios
    #

    DATA_DIR = "data"

    LOG_DIR = "logs"

    HISTORICO_FILE = (
        "data/ultimo_relatorio.json"
    )

###############################################################################
# Carteira
###############################################################################

CARTEIRA = [

    # Brasil

    "VALE3.SA",

    "PETR3.SA",

    "BBAS3.SA",

    "ITSA4.SA",

    "WEGE3.SA",

    "POMO3.SA",

    "AXIA3.SA",

    # ETFs EUA

    "VGT",

    "TFLO",

    "GLD",

    "RSP",

    "KWEB",

    # Cripto

    "BTC-USD",

    "SOL-USD"

]
###############################################################################
# Constantes
###############################################################################

MAX_TELEGRAM_MESSAGE = 4000

VERSAO = "1.0.0"

NOME_PROJETO = "Portfolio Agent"

AUTOR = "Helder Mendes"
