"""
telegram_sender.py
------------------

Responsável pelo envio do relatório ao Telegram.
"""

from __future__ import annotations

import logging
from typing import List

import requests

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import Config

logger = logging.getLogger(__name__)


class TelegramSender:

    LIMITE_MENSAGEM = 4000

    BASE_URL = "https://api.telegram.org"

    def __init__(self):

        if not Config.TELEGRAM_TOKEN:
            raise ValueError(
                "TELEGRAM_TOKEN não configurado."
            )

        if not Config.TELEGRAM_CHAT_ID:
            raise ValueError(
                "TELEGRAM_CHAT_ID não configurado."
            )

        self.url = (
            f"{self.BASE_URL}/bot"
            f"{Config.TELEGRAM_TOKEN}"
            "/sendMessage"
        )

        self.session = requests.Session()
          def dividir_mensagem(
        self,
        texto: str
    ) -> List[str]:

        if len(texto) <= self.LIMITE_MENSAGEM:
            return [texto]

        partes = []

        while len(texto) > self.LIMITE_MENSAGEM:

            corte = texto.rfind(
                "\n",
                0,
                self.LIMITE_MENSAGEM
            )

            if corte == -1:
                corte = self.LIMITE_MENSAGEM

            partes.append(
                texto[:corte]
            )

            texto = texto[corte:].lstrip()

        partes.append(texto)

        return partes
          @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2)
    )
    def enviar_parte(
        self,
        texto: str
    ):

        payload = {

            "chat_id":
                Config.TELEGRAM_CHAT_ID,

            "text":
                texto,

            "parse_mode":
                "Markdown"

        }

        resposta = self.session.post(

            self.url,

            data=payload,

           timeout=Config.TIMEOUT_HTTP

        )

        resposta.raise_for_status()

        return resposta.json()
         def enviar(
        self,
        mensagem: str
    ):

        partes = self.dividir_mensagem(
            mensagem
        )

        total = len(partes)

        respostas = []

        for indice, parte in enumerate(
            partes,
            start=1
        ):

            if total > 1:

                cabecalho = (
                    f"**Parte {indice}/{total}**\n\n"
                )

                parte = cabecalho + parte

            logger.info(
                "Enviando parte %s/%s",
                indice,
                total
            )

            respostas.append(

                self.enviar_parte(parte)

            )

        logger.info(
            "Telegram finalizado."
        )

        return respostas
    def enviar_resumo(
        self,
        resumo: str
    ):

        titulo = (
            "📊 *Resumo Executivo*\n\n"
        )

        return self.enviar(

            titulo + resumo

        )
          def enviar_relatorio(
        self,
        relatorio: str
    ):

        titulo = (
            "📈 *Relatório Técnico*\n\n"
        )

        return self.enviar(

            titulo + relatorio

        )
      def enviar_resumo(
    resumo: str
):

    TelegramSender().enviar_resumo(
        resumo
    )


def enviar_relatorio(
    relatorio: str
):

    TelegramSender().enviar_relatorio(
        relatorio
    )
