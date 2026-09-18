from __future__ import annotations

import json
import logging
from typing import Any

import google.generativeai as genai
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import Config

logger = logging.getLogger(__name__)

PROMPT = """
Você é um analista sênior de ações e gestão de carteira.

Responda em português, de forma simples, curta e direta.

Use somente os dados do JSON.

Para cada ativo, informe apenas:
- Ticker
- Ação: Aumentar posição, Comprar, Manter, Reduzir ou Vender
- Justificativa curta, em uma frase

Não escreva introdução, conclusão, ranking, tabela, emojis ou texto extra.
Não cite dados que não estejam no JSON.
Se faltar informação relevante, use apenas o que estiver disponível.
""".strip()


class GeminiClient:
    """Cliente de acesso ao Gemini para gerar o relatório textual."""

    def __init__(self) -> None:
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            getattr(Config, "GEMINI_MODEL", "gemini-2.5-pro")
        )

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2))
    def gerar_relatorio(self, carteira_json: dict[str, Any]) -> str:
        """Gera um relatório curto e objetivo a partir do JSON da carteira."""
        logger.info("Enviando dados ao Gemini...")

        texto = json.dumps(carteira_json, ensure_ascii=False, indent=2)

        resposta = self.model.generate_content(
            [PROMPT, texto],
            generation_config={
                "temperature": 0.2,
                "top_p": 0.9,
                "max_output_tokens": 4096,
            },
        )

        return str(getattr(resposta, "text", "")).strip()


def analisar_carteira(carteira_json: dict[str, Any]) -> str:
    """Função de conveniência para gerar o relatório com o Gemini."""
    cliente = GeminiClient()
    return cliente.gerar_relatorio(carteira_json)
