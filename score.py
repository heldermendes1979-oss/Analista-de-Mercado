"""
score.py
---------

Responsável pelo cálculo do Score Técnico.

Entrada:
    AnaliseTecnica

Saída:
    Score (0-100)
    Recomendação
"""

from __future__ import annotations

from indicadores import AnaliseTecnica


class ScoreTecnico:

    """
    Calcula um score entre 0 e 100 para um ativo.

    Quanto maior o score,
    melhor a configuração técnica.
    """

    @staticmethod
    def calcular(ativo: AnaliseTecnica):

        score = 0

        detalhes = []

        #################################################
        # Tendência Principal
        #################################################

        if ativo.ema20 > ativo.ema50:

            score += 15

            detalhes.append(
                "+15 EMA20 acima da EMA50"
            )

        if ativo.ema50 > ativo.ema200:

            score += 15

            detalhes.append(
                "+15 EMA50 acima da EMA200"
            )

        if ativo.preco > ativo.ema200:

            score += 10

            detalhes.append(
                "+10 Preço acima da EMA200"
            )

        #################################################
        # RSI
        #################################################

        if 40 <= ativo.rsi <= 65:

            score += 10

            detalhes.append(
                "+10 RSI saudável"
            )

        elif 30 <= ativo.rsi < 40:

            score += 8

            detalhes.append(
                "+8 RSI próximo da sobrevenda"
            )

        #################################################
        # ADX
        #################################################

        if ativo.adx >= 25:

            score += 10

            detalhes.append(
                "+10 Tendência forte (ADX)"
            )

        #################################################
        # MACD
        #################################################

        if ativo.macd > ativo.macd_signal:

            score += 10

            detalhes.append(
                "+10 MACD comprado"
            )

        #################################################
        # Volume
        #################################################

        if ativo.volume_relativo >= 1.10:

            score += 10

            detalhes.append(
                "+10 Volume acima da média"
            )

        #################################################
        # Distância da EMA20
        #################################################

        distancia = abs(ativo.distancia_ema20)

        if distancia <= 2:

            score += 10

            detalhes.append(
                "+10 Próximo da EMA20"
            )

        elif distancia <= 5:

            score += 5

            detalhes.append(
                "+5 Distância aceitável da EMA20"
            )

        #################################################
        # Volatilidade
        #################################################

        if ativo.risco_percentual <= 6:

            score += 10

            detalhes.append(
                "+10 Stop técnico curto"
            )

        #################################################
        # Limites
        #################################################

        score = max(0, min(score, 100))

        ativo.score = score

        ativo.recomendacao = (
            ScoreTecnico.classificar(score)
        )

        return score, detalhes

    @staticmethod
    def classificar(score: int):

        if score >= 90:
            return "★★★★★ Compra Forte"

        if score >= 80:
            return "★★★★ Compra"

        if score >= 65:
            return "★★★ Manter"

        if score >= 45:
            return "★★ Reduzir"

        return "★ Venda"

######################  Função para ordenar toda a carteira ################

def ranquear_carteira(lista):

    for ativo in lista:

        ScoreTecnico.calcular(ativo)

    return sorted(

        lista,

        key=lambda x: x.score,

        reverse=True

    )

#########################   Função para obter os melhores e piores ativos  #########################

def melhores_ativos(lista, quantidade=3):

    carteira = ranquear_carteira(lista)

    return carteira[:quantidade]

def piores_ativos(lista, quantidade=2):

    carteira = ranquear_carteira(lista)

    return carteira[-quantidade:]

from indicadores import analisar_ativo
from score import ScoreTecnico

ativo = analisar_ativo("VALE3.SA")

score, detalhes = ScoreTecnico.calcular(ativo)

print(score)

print(ativo.recomendacao)

print(detalhes)
