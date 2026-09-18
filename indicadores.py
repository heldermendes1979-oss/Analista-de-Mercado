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

    nome: str = ""
    classe: str = ""
    pais: str = ""
    moeda: str = ""
    setor: str = ""
    
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
def classificar_rsi(rsi: float) -> str:
    """
    Interpretação do RSI.
    """

    if np.isnan(rsi):
        return "Indefinido"

    if rsi < 30:
        return "Sobrevendido"

    if rsi < 40:
        return "Fraco"

    if rsi <= 65:
        return "Neutro"

    if rsi <= 70:
        return "Forte"

    return "Sobrecomprado"
def classificar_adx(adx: float) -> str:

    if np.isnan(adx):
        return "Indefinido"

    if adx < 20:
        return "Lateral"

    if adx < 25:
        return "Iniciando tendência"

    if adx < 40:
        return "Tendência Forte"

    return "Tendência Muito Forte"
def classificar_macd(macd: float,
                     signal: float) -> str:

    if np.isnan(macd) or np.isnan(signal):
        return "Indefinido"

    if macd > signal:
        return "Compra"

    return "Venda"
def classificar_volume(volume_relativo: float):

    if np.isnan(volume_relativo):
        return "Indefinido"

    if volume_relativo >= 1.50:
        return "Muito acima da média"

    if volume_relativo >= 1.15:
        return "Acima da média"

    if volume_relativo >= 0.85:
        return "Normal"

    return "Baixo"
def classificar_tendencia(
        preco,
        ema20,
        ema50,
        ema200):

    if (
        preco > ema20
        and ema20 > ema50
        and ema50 > ema200
    ):
        return "Alta Forte"

    if (
        preco > ema20
        and ema20 > ema50
    ):
        return "Alta"

    if (
        preco < ema20
        and ema20 < ema50
    ):
        return "Baixa"

    return "Lateral"
def classificar_distancia(dist):

    if np.isnan(dist):
        return "Indefinido"

    d = abs(dist)

    if d < 2:
        return "Excelente"

    if d < 5:
        return "Aceitável"

    if d < 8:
        return "Esticado"

    return "Muito Esticado"

###############################   Função principal   ############################

def analisar_ativo(ticker: str) -> AnaliseTecnica:

    df = baixar_dados(ticker)

    df = calcular_indicadores(df)

    ultimo = df.iloc[-1]

    preco = float(ultimo["Close"])

    tendencia = classificar_tendencia(
        preco,
        ultimo["EMA20"],
        ultimo["EMA50"],
        ultimo["EMA200"]
    )

    return AnaliseTecnica(

        ticker=ticker,

        preco=preco,

        tendencia=tendencia,

        ema20=float(ultimo["EMA20"]),
        ema50=float(ultimo["EMA50"]),
        ema200=float(ultimo["EMA200"]),

        rsi=float(ultimo["RSI"]),

        atr=float(ultimo["ATR"]),

        adx=float(ultimo["ADX"]),

        macd=float(ultimo["MACD"]),

        macd_signal=float(
            ultimo["MACD_SIGNAL"]
        ),

        macd_hist=float(
            ultimo["MACD_HIST"]
        ),

        obv=float(
            ultimo["OBV"]
        ),

        bb_high=float(
            ultimo["BB_HIGH"]
        ),

        bb_mid=float(
            ultimo["BB_MID"]
        ),

        bb_low=float(
            ultimo["BB_LOW"]
        ),

        volume=float(
            ultimo["Volume"]
        ),

        volume_medio20=float(
            ultimo["VOLUME20"]
        ),

        volume_relativo=float(
            ultimo["VOLUME_REL"]
        ),

        distancia_ema20=float(
            ultimo["DIST_EMA20"]
        ),

        suporte=float(
            ultimo["SUPORTE"]
        ),

        resistencia=float(
            ultimo["RESISTENCIA"]
        ),

        retorno_semana=float(
            ultimo["RET_SEMANA"]
        ),

        retorno_mes=float(
            ultimo["RET_MES"]
        ),

        volatilidade=float(
            ultimo["VOL"]
        ),

        stop_loss=float(
            ultimo["STOP"]
        ),

        risco_percentual=float(
            ultimo["RISCO"]
        )
    )

##############################   Conversão para JSON  ############################

def to_dict(
    analise: AnaliseTecnica
) -> Dict[str, Any]:

    return {

        "ticker": analise.ticker,

        "preco": analise.preco,

        "tendencia": analise.tendencia,

        "rsi": analise.rsi,

        "rsi_status":
            classificar_rsi(
                analise.rsi
            ),

        "adx": analise.adx,

        "adx_status":
            classificar_adx(
                analise.adx
            ),

        "macd": analise.macd,

        "macd_signal":
            analise.macd_signal,

        "macd_status":
            classificar_macd(
                analise.macd,
                analise.macd_signal
            ),

        "volume_relativo":
            analise.volume_relativo,

        "volume_status":
            classificar_volume(
                analise.volume_relativo
            ),

        "ema20":
            analise.ema20,

        "ema50":
            analise.ema50,

        "ema200":
            analise.ema200,

        "distancia_ema20":
            analise.distancia_ema20,

        "distancia_status":
            classificar_distancia(
                analise.distancia_ema20
            ),

        "bb_high":
            analise.bb_high,

        "bb_mid":
            analise.bb_mid,

        "bb_low":
            analise.bb_low,

        "stop":
            analise.stop_loss,

        "risco":
            analise.risco_percentual,

        "suporte":
            analise.suporte,

        "resistencia":
            analise.resistencia,

        "retorno_semana":
            analise.retorno_semana,

        "retorno_mes":
            analise.retorno_mes,

        "volatilidade":
            analise.volatilidade
        
        "score":

            analise.score,

        "recomendacao":
            analise.recomendacao,
    }

