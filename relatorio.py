from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import Config
from indicadores import AnaliseTecnica, to_dict


def _acao_por_score(score: int) -> str:
    """Converte score técnico em ação operacional curta."""
    if score >= 90:
        return "Aumentar posição"
    if score >= 80:
        return "Comprar"
    if score >= 65:
        return "Manter"
    if score >= 45:
        return "Reduzir"
    return "Vender"


class Relatorio:
    """Organiza os ativos analisados e gera o JSON final da carteira."""

    def __init__(self) -> None:
        self.ativos: list[AnaliseTecnica] = []

    def ordenar(self) -> None:
        """Ordena os ativos por score, do maior para o menor."""
        self.ativos.sort(key=lambda ativo: getattr(ativo, "score", 0), reverse=True)

    def estatisticas(self) -> dict[str, Any]:
        """Calcula estatísticas resumidas da carteira."""
        total = len(self.ativos)
        score_total = 0

        compra_forte = 0
        compra = 0
        manter = 0
        reduzir = 0
        venda = 0

        for ativo in self.ativos:
            score = int(getattr(ativo, "score", 0))
            score_total += score

            if score >= 90:
                compra_forte += 1
            elif score >= 80:
                compra += 1
            elif score >= 65:
                manter += 1
            elif score >= 45:
                reduzir += 1
            else:
                venda += 1

        media = round(score_total / total, 1) if total else 0.0

        return {
            "total_ativos": total,
            "score_medio": media,
            "compra_forte": compra_forte,
            "compra": compra,
            "manter": manter,
            "reduzir": reduzir,
            "venda": venda,
        }

    def gerar_json(self) -> dict[str, Any]:
        """Gera o JSON final da carteira, já ordenado por score."""
        self.ordenar()

        ativos_json = [to_dict(ativo) for ativo in self.ativos]

        return {
            "data": datetime.now().strftime("%Y-%m-%d"),
            "estatisticas": self.estatisticas(),
            "ativos": ativos_json,
        }

    def salvar_json(
        self,
        dados: dict[str, Any],
        arquivo: str | Path | None = None,
    ) -> None:
        """Salva o JSON final em disco."""
        destino = Path(arquivo or Config.HISTORICO_FILE)
        destino.parent.mkdir(parents=True, exist_ok=True)

        with destino.open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_relatorio_anterior(
    arquivo: str | Path | None = None,
) -> dict[str, Any] | None:
    """Carrega o último relatório salvo, se existir."""
    caminho = Path(arquivo or Config.HISTORICO_FILE)

    if not caminho.exists():
        return None

    with caminho.open(encoding="utf-8") as f:
        return json.load(f)


def comparar(
    atual: dict[str, Any],
    anterior: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    """Compara o relatório atual com o anterior e retorna as variações."""
    if not anterior:
        return []

    antigos = {
        item["ticker"]: item
        for item in anterior.get("ativos", [])
        if "ticker" in item
    }

    mudancas: list[dict[str, Any]] = []

    for ativo in atual.get("ativos", []):
        ticker = ativo.get("ticker")
        if not ticker or ticker not in antigos:
            continue

        antigo = antigos[ticker]
        score_anterior = int(antigo.get("score", 0))
        score_atual = int(ativo.get("score", 0))

        mudancas.append(
            {
                "ticker": ticker,
                "score_anterior": score_anterior,
                "score_atual": score_atual,
                "variacao_score": score_atual - score_anterior,
                "tendencia_anterior": antigo.get("tendencia", ""),
                "tendencia_atual": ativo.get("tendencia", ""),
                "acao_anterior": _acao_por_score(score_anterior),
                "acao_atual": _acao_por_score(score_atual),
            }
        )

    return mudancas
