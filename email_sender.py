"""
email_sender.py
---------------

Responsável pelo envio do relatório por e-mail.
"""

from __future__ import annotations

import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from config import Config

logger = logging.getLogger(__name__)


class EmailSender:

    def __init__(self):

        if not Config.EMAIL_USER:
            raise ValueError(
                "EMAIL_USER não configurado."
            )

        if not Config.EMAIL_PASS:
            raise ValueError(
                "EMAIL_PASS não configurado."
            )

        if not Config.EMAIL_DESTINO:
            raise ValueError(
                "EMAIL_DESTINO não configurado."
            )

      #################################   Criação da mensagem    ##############################

    def criar_email(
        self,
        assunto: str,
        corpo: str
    ):

        msg = MIMEMultipart()

        msg["From"] = Config.EMAIL_USER

        msg["To"] = Config.EMAIL_DESTINO

        msg["Subject"] = assunto

        msg.attach(

            MIMEText(

                corpo,

                "plain",

                "utf-8"

            )

        )

        return msg
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2)
    )
    def enviar(
        self,
        assunto: str,
        corpo: str
    ):

        mensagem = self.criar_email(

            assunto,

            corpo

        )

        with smtplib.SMTP(

            "Config.SMTP_SERVER",

            587,

            timeout=30

        ) as smtp:

            smtp.starttls()

            smtp.login(

                Config.EMAIL_USER,

                Config.EMAIL_PASS

            )

            smtp.sendmail(

                Config.EMAIL_USER,

                Config.EMAIL_DESTINO,

                mensagem.as_string()

            )

        logger.info(

            "E-mail enviado com sucesso."

        )
          def enviar_relatorio(
        self,
        relatorio: str
    ):

        assunto = (

            "Boletim Diário da Carteira"

        )

        self.enviar(

            assunto,

            relatorio

        )
      def enviar_relatorio(

    relatorio: str

):

    EmailSender().enviar_relatorio(

        relatorio

    )
