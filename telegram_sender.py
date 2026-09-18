from __future__ import annotations

import logging
from typing import Any

import requests
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import Config, MAX_TELEGRAM_MESSAGE

logger = logging.getLogger(__name__)


class TelegramSender:
    """Envia mensagens ao Telegram, com divisão automática quando necessário."""

    def __init__(self) -> None:
        if not Config.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN não configurado.")

        if not Config.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID não configurado.")

        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"
        self.session = requests.Session()

    def _quebrar_mensagem(self, mensagem: str) -> list[str]:
        """
        Divide mensagens longas em blocos seguros para o Telegram.
        Tenta quebrar por linha; se não for possível, corta no limite.
        """
        limite = max(1000, MAX_TELEGRAM_MESSAGE - 200)

        if len(mensagem) <= limite:
            return [mensagem]

        partes: list[str] = []
        restante = mensagem.strip()

        while len(restante) > limite:
            corte = restante.rfind("\n", 0, limite)
            if corte <= 0:
                corte = limite

            partes.append(restante[:corte].strip())
            restante = restante[corte:].strip()

        if restante:
            partes.append(restante)

        return partes

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2))
    def _enviar_parte(self, texto: str) -> dict[str, Any]:
        payload = {
            "chat_id": self.chat_id,
            "text": texto,
        }

        resposta = self.session.post(
            self.url,
            data=payload,
            timeout=Config.TIMEOUT_HTTP,
        )
        resposta.raise_for_status()
        return resposta.json()

    def enviar(self, mensagem: str) -> list[dict[str, Any]]:
        """
        Envia uma mensagem, dividindo automaticamente se exceder o limite.
        """
        partes = self._quebrar_mensagem(mensagem)
        total = len(partes)
        respostas: list[dict[str, Any]] = []

        for indice, parte in enumerate(partes, start=1):
            if total > 1:
                parte = f"Parte {indice}/{total}\n\n{parte}"

            logger.info("Enviando mensagem ao Telegram (%s/%s)", indice, total)
            respostas.append(self._enviar_parte(parte))

        return respostas

    def enviar_resumo(self, resumo: str) -> list[dict[str, Any]]:
        """Envia o resumo executivo."""
        mensagem = f"RESUMO EXECUTIVO\n\n{resumo}"
        return self.enviar(mensagem)

    def enviar_relatorio(self, relatorio: str) -> list[dict[str, Any]]:
        """Envia o relatório completo."""
        mensagem = f"RELATÓRIO TÉCNICO\n\n{relatorio}"
        return self.enviar(mensagem)


def enviar_resumo(resumo: str) -> list[dict[str, Any]]:
    """Interface pública para envio do resumo executivo."""
    return TelegramSender().enviar_resumo(resumo)


def enviar_relatorio(relatorio: str) -> list[dict[str, Any]]:
    """Interface pública para envio do relatório completo."""
    return TelegramSender().enviar_relatorio(relatorio)
