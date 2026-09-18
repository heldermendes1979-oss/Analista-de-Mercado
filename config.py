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

    # ===========================
    # AÇÕES BRASIL
    # ===========================

    {
        "ticker": "VALE3.SA",
        "nome": "Vale",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Mineração"
    },

    {
        "ticker": "PETR3.SA",
        "nome": "Petrobras ON",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Petróleo"
    },

    {
        "ticker": "BBAS3.SA",
        "nome": "Banco do Brasil",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Financeiro"
    },

    {
        "ticker": "ITSA4.SA",
        "nome": "Itaúsa",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Holding"
    },

    {
        "ticker": "WEGE3.SA",
        "nome": "WEG",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Industrial"
    },

    {
        "ticker": "POMO3.SA",
        "nome": "Marcopolo",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Industrial"
    },

    {
        "ticker": "AXIA3.SA",
        "nome": "Axia",
        "classe": "Ação",
        "pais": "Brasil",
        "moeda": "BRL",
        "setor": "Tecnologia"
    },

    # ===========================
    # ETFs EUA
    # ===========================

    {
        "ticker": "VGT",
        "nome": "Vanguard Information Technology ETF",
        "classe": "ETF",
        "pais": "Estados Unidos",
        "moeda": "USD",
        "setor": "Tecnologia"
    },

    {
        "ticker": "TFLO",
        "nome": "iShares Treasury Floating Rate Bond ETF",
        "classe": "ETF",
        "pais": "Estados Unidos",
        "moeda": "USD",
        "setor": "Renda Fixa"
    },

    {
        "ticker": "GLD",
        "nome": "SPDR Gold Shares",
        "classe": "ETF",
        "pais": "Estados Unidos",
        "moeda": "USD",
        "setor": "Ouro"
    },

    {
        "ticker": "RSP",
        "nome": "Invesco S&P 500 Equal Weight",
        "classe": "ETF",
        "pais": "Estados Unidos",
        "moeda": "USD",
        "setor": "Índice"
    },

    {
        "ticker": "KWEB",
        "nome": "KraneShares CSI China Internet ETF",
        "classe": "ETF",
        "pais": "China",
        "moeda": "USD",
        "setor": "Internet"
    },

    # ===========================
    # Cripto
    # ===========================

    {
        "ticker": "BTC-USD",
        "nome": "Bitcoin",
        "classe": "Criptomoeda",
        "pais": "Global",
        "moeda": "USD",
        "setor": "Cripto"
    },

    {
        "ticker": "SOL-USD",
        "nome": "Solana",
        "classe": "Criptomoeda",
        "pais": "Global",
        "moeda": "USD",
        "setor": "Cripto"
    }

]
###############################################################################
# Constantes
###############################################################################

MAX_TELEGRAM_MESSAGE = 4000

VERSAO = "1.0.0"

NOME_PROJETO = "Portfolio Agent"

AUTOR = "Helder Mendes"
