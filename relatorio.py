"""
relatorio.py
------------

Responsável por:

• Organizar a carteira
• Gerar estatísticas
• Gerar o JSON
• Salvar o último relatório
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from indicadores import (
    AnaliseTecnica,
    to_dict
)

from score import (
    ScoreTecnico,
    ranquear_carteira
)


class Relatorio:

    def __init__(self):

        self.ativos = []

    def estatisticas(self):

        total = len(self.ativos)

        score_total = 0

        compra_forte = 0
        compra = 0
        manter = 0
        reduzir = 0
        venda = 0

        for ativo in self.ativos:

            score_total += ativo.score

            if ativo.score >= 90:

                compra_forte += 1

            elif ativo.score >= 80:

                compra += 1

            elif ativo.score >= 65:

                manter += 1

            elif ativo.score >= 45:

                reduzir += 1

            else:

                venda += 1

        media = 0

        if total:

            media = score_total / total

        return {

            "total_ativos": total,

            "score_medio": round(media, 1),

            "compra_forte": compra_forte,

            "compra": compra,

            "manter": manter,

            "reduzir": reduzir,

            "venda": venda

        }

    def gerar_json(self):

        self.ativos = ranquear_carteira(self.ativos)

        ativos_json = [

            to_dict(ativo)

            for ativo in self.ativos

        ]

        return {

            "data":

                datetime.now().strftime("%Y-%m-%d"),

            "estatisticas":

                self.estatisticas(),

            "ativos":

                ativos_json

        }

    def salvar(

        self,

        arquivo="data/ultimo_relatorio.json"

    ):

        Path("data").mkdir(

            exist_ok=True

        )

        dados = self.gerar_json()

        with open(

            arquivo,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                dados,

                f,

                ensure_ascii=False,

                indent=4

            )

        return dados
     def carregar_relatorio_anterior(

    arquivo="data/ultimo_relatorio.json"

):

    path = Path(arquivo)

    if not path.exists():

        return None

    with open(

        path,

        encoding="utf-8"

    ) as f:

        return json.load(f)
def comparar(

    atual,

    anterior

):

    if anterior is None:

        return []

    antigos = {

        ativo["ticker"]: ativo

        for ativo in anterior["ativos"]

    }

    mudancas = []

    for ativo in atual["ativos"]:

        ticker = ativo["ticker"]

        if ticker not in antigos:

            continue

        antigo = antigos[ticker]

        mudancas.append({

            "ticker": ticker,

            "score_anterior":

                antigo["score"],

            "score_atual":

                ativo["score"],

            "variacao_score":

                ativo["score"] -

                antigo["score"],

            "tendencia_anterior":

                antigo["tendencia"],

            "tendencia_atual":

                ativo["tendencia"]

        })

    return mudancas
def gerar_relatorio(carteira):

    relatorio = Relatorio()

    for ativo in carteira:

        ScoreTecnico.calcular(ativo)

        relatorio.ativos.append(ativo)

    atual = relatorio.gerar_json()

    anterior = carregar_relatorio_anterior()

    atual["mudancas"] = comparar(

        atual,

        anterior

    )

    relatorio.salvar()

    return atual
def salvar_json(

    self,

    dados,

    arquivo="data/ultimo_relatorio.json"

):

    Path("data").mkdir(

        exist_ok=True

    )

    with open(

        arquivo,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            dados,

            f,

            ensure_ascii=False,

            indent=4

        )
