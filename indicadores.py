"""
indicadores.py
----------------

Responsável por:

• Download dos dados do Yahoo Finance
• Tratamento de erros
• Cálculo dos indicadores técnicos
• Retorno de um dicionário padronizado para os demais módulos

Autor: Portfolio Agent
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Any

import numpy as np
import pandas as pd
import ta
import yfinance as yf

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

logger = logging.getLogger(__name__)

############################ Classe de retorno #######################

@dataclass
class AnaliseTecnica:

    ticker: str

    preco: float

    tendencia: str

    score: int = 0

    recomendacao: str = ""

    ema20: float = np.nan
    ema50: float = np.nan
    ema200: float = np.nan

    rsi: float = np.nan

    atr: float = np.nan

    adx: float = np.nan

    macd: float = np.nan

    macd_signal: float = np.nan

    macd_hist: float = np.nan

    obv: float = np.nan

    bb_high: float = np.nan

    bb_mid: float = np.nan

    bb_low: float = np.nan

    volume: float = np.nan

    volume_medio20: float = np.nan

    volume_relativo: float = np.nan

    distancia_ema20: float = np.nan

    suporte: float = np.nan

    resistencia: float = np.nan

    retorno_semana: float = np.nan

    retorno_mes: float = np.nan

    volatilidade: float = np.nan

    stop_loss: float = np.nan

    risco_percentual: float = np.nan

#########################    Download dos dados    ###################

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2)
)
def baixar_dados(ticker: str,
                 periodo: str = "12mo") -> pd.DataFrame:

    logger.info(f"Baixando {ticker}")

    df = yf.download(
        ticker,
        period=periodo,
        progress=False,
        auto_adjust=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    if df.empty:
        raise ValueError(f"{ticker} sem dados")

    return df

#######################################  Indicadores  #######################

def calcular_indicadores(df: pd.DataFrame):

    close = df["Close"]

    high = df["High"]

    low = df["Low"]

    volume = df["Volume"]

    #
    # Médias
    #

    df["EMA20"] = ta.trend.ema_indicator(
        close,
        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(
        close,
        window=50
    )

    df["EMA200"] = ta.trend.ema_indicator(
        close,
        window=200
    )

    #
    # RSI
    #

    df["RSI"] = ta.momentum.rsi(
        close,
        window=14
    )

    #
    # ATR
    #

    df["ATR"] = ta.volatility.average_true_range(
        high,
        low,
        close,
        window=14
    )

    #
    # ADX
    #

    df["ADX"] = ta.trend.adx(
        high,
        low,
        close,
        window=14
    )

    #
    # MACD
    #

    macd = ta.trend.MACD(close)

    df["MACD"] = macd.macd()

    df["MACD_SIGNAL"] = macd.macd_signal()

    df["MACD_HIST"] = macd.macd_diff()

    #
    # Bollinger
    #

    bb = ta.volatility.BollingerBands(close)

    df["BB_HIGH"] = bb.bollinger_hband()

    df["BB_MID"] = bb.bollinger_mavg()

    df["BB_LOW"] = bb.bollinger_lband()

    #
    # OBV
    #

    df["OBV"] = ta.volume.on_balance_volume(
        close,
        volume
    )

########################  Demais Indicadores  #######################

     df["VOLUME20"] = volume.rolling(20).mean()

    df["VOLUME_REL"] = (
        volume /
        df["VOLUME20"]
    )
    df["DIST_EMA20"] = (
        (close - df["EMA20"])
        /
        df["EMA20"]
    ) * 100
    df["SUPORTE"] = (
        low
        .rolling(20)
        .min()
    )

    df["RESISTENCIA"] = (
        high
        .rolling(20)
        .max()
    )
    df["RET_SEMANA"] = (
        close.pct_change(5)
    ) * 100

    df["RET_MES"] = (
        close.pct_change(21)
    ) * 100
    retorno = np.log(
        close /
        close.shift(1)
    )

    df["VOL"] = (
        retorno
        .rolling(21)
        .std()
        * np.sqrt(252)
        * 100
    )
    df["STOP"] = (
        close
        - 2 * df["ATR"]
    )

    df["RISCO"] = (
        (close - df["STOP"])
        /
        close
        * 100
    )

    return df
