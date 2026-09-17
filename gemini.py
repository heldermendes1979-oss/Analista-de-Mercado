"""
gemini.py
----------

Responsável pela comunicação com o Gemini.

Entrada:
    JSON da carteira

Saída:
    Relatório executivo em Markdown
"""

from __future__ import annotations

import json
import logging

import google.generativeai as genai

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import Config

logger = logging.getLogger(__name__)

################################# Inicialização ########################

class GeminiClient:

    def __init__(self):

        if not Config.GEMINI_API_KEY:

            raise ValueError(
                "GEMINI_API_KEY não configurada."
            )

        genai.configure(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-pro"
        )

  #####################################  Prompt Institucional  ########################

PROMPT = """
Você é um Analista Sênior de Investimentos com experiência em Asset Management.

Seu papel é atuar como gestor da carteira do usuário.

Utilize EXCLUSIVAMENTE os indicadores fornecidos.

Não invente números.

Não faça previsões sem suporte técnico.

Produza um relatório profissional.

========================

Estrutura obrigatória

1 - RESUMO EXECUTIVO

Explique:

• panorama geral da carteira

• força da tendência

• distribuição dos ativos

• riscos

• oportunidades

========================

2 - RANKING

Classifique todos os ativos
do melhor para o pior.

Utilize o Score Técnico.

========================

3 - ANÁLISE INDIVIDUAL

Para cada ativo informe:

Ticker

Preço Atual

Score Técnico

Tendência

RSI

Interpretação do RSI

ADX

MACD

Volume Relativo

Distância EMA20

Stop Loss

Suporte

Resistência

Risco

Recomendação

Justificativa em até cinco linhas.

========================

4 - AÇÕES PRIORITÁRIAS

Liste:

Os três melhores ativos
para aumento de posição.

Os dois ativos
que merecem atenção.

========================

5 - CONCLUSÃO

Explique em linguagem de um relatório de research.

Nunca utilize emojis.

Nunca escreva em primeira pessoa.

Sempre utilize Markdown.

"""

###################################  Chamada da API  ############################

@retry(

    stop=stop_after_attempt(5),

    wait=wait_exponential(multiplier=2)

)
def gerar_relatorio(

    self,

    carteira_json: dict

):

    logger.info(
        "Enviando dados ao Gemini..."
    )

    texto = json.dumps(

        carteira_json,

        indent=4,

        ensure_ascii=False

    )

    resposta = self.model.generate_content(

        PROMPT + "\n\n" + texto

    )

    return resposta.text

def analisar_carteira(

    carteira_json

):

    cliente = GeminiClient()

    return cliente.gerar_relatorio(

        carteira_json

    )
