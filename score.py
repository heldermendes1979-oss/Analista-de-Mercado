from __future__ import annotations

from typing import Any

from indicadores import AnaliseTecnica


class ScoreTecnico:
    """Calcula score técnico e recomendação a partir da análise consolidada."""

    @staticmethod
    def calcular(ativo: AnaliseTecnica) -> tuple[int, list[str]]:
        score = 0
        detalhes: list[str] = []

        # Tendência principal
        if ativo.ema20 > ativo.ema50:
            score += 15
            detalhes.append("+15 EMA20 acima da EMA50")

        if ativo.ema50 > ativo.ema200:
            score += 15
            detalhes.append("+15 EMA50 acima da EMA200")

        if ativo.preco > ativo.ema200:
            score += 10
            detalhes.append("+10 Preço acima da EMA200")

        # RSI
        if 40 <= ativo.rsi <= 65:
            score += 10
            detalhes.append("+10 RSI saudável")
        elif 30 <= ativo.rsi < 40:
            score += 8
            detalhes.append("+8 RSI próximo da sobrevenda")

        # ADX
        if ativo.adx >= 25:
            score += 10
            detalhes.append("+10 Tendência forte (ADX)")

        # MACD
        if ativo.macd > ativo.macd_signal:
            score += 10
            detalhes.append("+10 MACD comprado")

        # Volume
        if ativo.volume_relativo >= 1.10:
            score += 10
            detalhes.append("+10 Volume acima da média")

        # Distância da EMA20
        distancia = abs(ativo.distancia_ema20)

        if distancia <= 2:
            score += 10
            detalhes.append("+10 Próximo da EMA20")
        elif distancia <= 5:
            score += 5
            detalhes.append("+5 Distância aceitável da EMA20")

        # Volatilidade / risco técnico
        if ativo.risco_percentual <= 6:
            score += 10
            detalhes.append("+10 Stop técnico curto")

        score = max(0, min(score, 100))
        ativo.score = score
        ativo.recomendacao = ScoreTecnico.classificar(score)

        return score, detalhes

    @staticmethod
    def classificar(score: int) -> str:
        if score >= 90:
            return "★★★★★ Compra Forte"
        if score >= 80:
            return "★★★★ Compra"
        if score >= 65:
            return "★★★ Manter"
        if score >= 45:
            return "★★ Reduzir"
        return "★ Venda"


def ranquear_carteira(lista: list[AnaliseTecnica]) -> list[AnaliseTecnica]:
    """Calcula o score de todos os ativos e retorna a carteira ordenada."""
    for ativo in lista:
        ScoreTecnico.calcular(ativo)

    return sorted(lista, key=lambda x: x.score, reverse=True)


def melhores_ativos(lista: list[AnaliseTecnica], quantidade: int = 3) -> list[AnaliseTecnica]:
    """Retorna os melhores ativos da carteira."""
    carteira = ranquear_carteira(lista)
    return carteira[:quantidade]


def piores_ativos(lista: list[AnaliseTecnica], quantidade: int = 2) -> list[AnaliseTecnica]:
    """Retorna os piores ativos da carteira."""
    carteira = ranquear_carteira(lista)
    return carteira[-quantidade:]
