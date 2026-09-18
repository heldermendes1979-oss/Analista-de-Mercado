from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from models import AtivoConfig

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Configurações centralizadas do Portfolio Agent."""

    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

    TELEGRAM_TOKEN: str | None = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_PARSE_MODE: str = os.getenv("TELEGRAM_PARSE_MODE", "Markdown")

    EMAIL_USER: str | None = os.getenv("EMAIL_USER")
    EMAIL_PASS: str | None = os.getenv("EMAIL_PASS")
    EMAIL_DESTINO: str | None = os.getenv("EMAIL_DESTINO")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))

    CACHE_DIAS: int = int(os.getenv("CACHE_DIAS", "180"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    TIMEOUT_HTTP: int = int(os.getenv("TIMEOUT_HTTP", "30"))

    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    HISTORICO_FILE: str = os.getenv("HISTORICO_FILE", "data/ultimo_relatorio.json")


CARTEIRA: list[AtivoConfig] = [
    AtivoConfig(
        ticker="VALE3.SA",
        nome="Vale",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Mineração",
    ),
    AtivoConfig(
        ticker="PETR3.SA",
        nome="Petrobras ON",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Petróleo",
    ),
    AtivoConfig(
        ticker="BBAS3.SA",
        nome="Banco do Brasil",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Financeiro",
    ),
    AtivoConfig(
        ticker="ITSA4.SA",
        nome="Itaúsa",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Holding",
    ),
    AtivoConfig(
        ticker="WEGE3.SA",
        nome="WEG",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Industrial",
    ),
    AtivoConfig(
        ticker="POMO3.SA",
        nome="Marcopolo",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Industrial",
    ),
    AtivoConfig(
        ticker="AXIA3.SA",
        nome="Axia",
        classe="Ação",
        pais="Brasil",
        moeda="BRL",
        setor="Tecnologia",
    ),
    AtivoConfig(
        ticker="VGT",
        nome="Vanguard Information Technology ETF",
        classe="ETF",
        pais="Estados Unidos",
        moeda="USD",
        setor="Tecnologia",
    ),
    AtivoConfig(
        ticker="TFLO",
        nome="iShares Treasury Floating Rate Bond ETF",
        classe="ETF",
        pais="Estados Unidos",
        moeda="USD",
        setor="Renda Fixa",
    ),
    AtivoConfig(
        ticker="GLD",
        nome="SPDR Gold Shares",
        classe="ETF",
        pais="Estados Unidos",
        moeda="USD",
        setor="Ouro",
    ),
    AtivoConfig(
        ticker="RSP",
        nome="Invesco S&P 500 Equal Weight",
        classe="ETF",
        pais="Estados Unidos",
        moeda="USD",
        setor="Índice",
    ),
    AtivoConfig(
        ticker="KWEB",
        nome="KraneShares CSI China Internet ETF",
        classe="ETF",
        pais="China",
        moeda="USD",
        setor="Internet",
    ),
    AtivoConfig(
        ticker="BTC-USD",
        nome="Bitcoin",
        classe="Criptomoeda",
        pais="Global",
        moeda="USD",
        setor="Cripto",
    ),
    AtivoConfig(
        ticker="SOL-USD",
        nome="Solana",
        classe="Criptomoeda",
        pais="Global",
        moeda="USD",
        setor="Cripto",
    ),
]

MAX_TELEGRAM_MESSAGE: int = 4000
VERSAO: str = "1.0.0"
NOME_PROJETO: str = "Portfolio Agent"
AUTOR: str = "Helder Mendes"
