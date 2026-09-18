##############  analise_ticket parte 1 #############################

"""
analise_ticket.py
-----------------

Programa principal do Portfolio Agent.

Fluxo:

1. Carrega configurações
2. Analisa todos os ativos
3. Calcula Score
4. Gera JSON
5. Envia ao Gemini
6. Envia Telegram
7. Envia E-mail
8. Salva histórico

Autor: Helder Mendes / ChatGPT
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from colorlog import ColoredFormatter

from config import CARTEIRA

from indicadores import analisar_ativo

from score import ScoreTecnico

from relatorio import (
    Relatorio,
    comparar,
    carregar_relatorio_anterior
)

from gemini import analisar_carteira

from telegram_sender import (
    enviar_resumo,
    enviar_relatorio
)

from email_sender import (
    enviar_relatorio as enviar_email
)

Path(Config.LOG_DIR)

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "portfolio.log"

logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = ColoredFormatter(

    "%(log_color)s%(levelname)-8s%(reset)s %(message)s"

)

console = logging.StreamHandler(sys.stdout)

console.setFormatter(formatter)

arquivo = logging.FileHandler(

    LOG_FILE,

    encoding="utf-8"

)

arquivo.setFormatter(

    logging.Formatter(

        "%(asctime)s %(levelname)s %(message)s"

    )

)

logger.addHandler(console)

logger.addHandler(arquivo)

class PortfolioAgent:

    def __init__(self):

        self.carteira = []

        self.relatorio = Relatorio()

      def analisar(self):

        logger.info(

            "Iniciando análise da carteira..."

        )

        for ticker in CARTEIRA:

            try:

                logger.info(

                    "Analisando %s",

                    ticker

                )

                    ticker = item["ticker"]

                    ativo = analisar_ativo(ticker)

                    ativo.nome = item["nome"]

                    ativo.classe = item["classe"]

                    ativo.pais = item["pais"]

                    ativo.moeda = item["moeda"]

                    ativo.setor = item["setor"]

    ScoreTecnico.calcular(ativo)

    self.carteira.append(ativo)
                ScoreTecnico.calcular(

                    ativo

                )

                self.carteira.append(

                    ativo

                )

            except Exception as erro:

                logger.exception(

                    "Erro em %s",

                    ticker

                )

        logger.info(

            "Carteira analisada."

        )

    def montar_relatorio(self):

        anterior = carregar_relatorio_anterior()

        self.relatorio.ativos = self.carteira

        atual = self.relatorio.gerar_json()

        atual["mudancas"] = comparar(

            atual,

            anterior

        )

        self.relatorio.salvar()

        return atual

############################### Parte 2 - Resumo Executivo  ##################################

    def gerar_resumo(self, dados):

        estat = dados["estatisticas"]

        melhores = dados["ativos"][:3]

        piores = dados["ativos"][-2:]

        linhas = []

        linhas.append("RESUMO EXECUTIVO")
        linhas.append("")
        linhas.append(
            f"Data: {dados['data']}"
        )

        linhas.append(
            f"Score Médio: {estat['score_medio']}"
        )

        linhas.append(
            f"Ativos analisados: {estat['total_ativos']}"
        )

        linhas.append("")

        linhas.append("Classificação")

        linhas.append(
            f"Compra Forte: {estat['compra_forte']}"
        )

        linhas.append(
            f"Compra: {estat['compra']}"
        )

        linhas.append(
            f"Manter: {estat['manter']}"
        )

        linhas.append(
            f"Reduzir: {estat['reduzir']}"
        )

        linhas.append(
            f"Venda: {estat['venda']}"
        )

        linhas.append("")

        linhas.append(
            "Top 3 Ativos"
        )

        for ativo in melhores:

            linhas.append(

                f"{ativo['ticker']} "
                f"({ativo['score']})"

            )

        linhas.append("")

        linhas.append(
            "Ativos que exigem atenção"
        )

        for ativo in piores:

            linhas.append(

                f"{ativo['ticker']} "
                f"({ativo['score']})"

            )

        return "\n".join(linhas)
          def gerar_relatorio_gemini(
        self,
        dados
    ):

        logger.info(

            "Solicitando análise ao Gemini..."

        )

        try:

            texto = analisar_carteira(

                dados

            )

            logger.info(

                "Relatório recebido."

            )

            return texto

        except Exception:

            logger.exception(

                "Erro ao consultar Gemini."

            )

            return (
                "Falha ao gerar o relatório "
                "executivo pelo Gemini."
            )
              def enviar_telegram(
        self,
        resumo,
        relatorio
    ):

        logger.info(

            "Enviando Telegram..."

        )

        try:

            enviar_resumo(

                resumo

            )

            enviar_relatorio(

                relatorio

            )

            logger.info(

                "Telegram enviado."

            )

        except Exception:

            logger.exception(

                "Erro Telegram."

            )
    def enviar_email(
        self,
        relatorio
    ):

        logger.info(

            "Enviando e-mail..."

        )

        try:

            enviar_email(

                relatorio

            )

            logger.info(

                "E-mail enviado."

            )

        except Exception:

            logger.exception(

                "Erro no envio do e-mail."

            )
    def executar(self):

        logger.info(

            "Portfolio Agent iniciado."

        )

        self.analisar()

        dados = self.montar_relatorio()

        resumo = self.gerar_resumo(

            dados

        )

        relatorio = (

            self.gerar_relatorio_gemini(

                dados

            )

        )

        self.enviar_telegram(

            resumo,

            relatorio

        )

        self.enviar_email(

            relatorio

        )

        logger.info(

            "Processo concluído."

        )

########################################### Parte 3 - Relatório Técnico de COntingência #############################

    def gerar_relatorio_local(
        self,
        dados
    ):

        linhas = []

        linhas.append("# RELATÓRIO TÉCNICO")
        linhas.append("")
        linhas.append(
            f"Data: {dados['data']}"
        )

        linhas.append("")

        for ativo in dados["ativos"]:

            linhas.append(
                f"## {ativo['ticker']}"
            )

            linhas.append(
                f"Preço: {ativo['preco']:.2f}"
            )

            linhas.append(
                f"Score: {ativo['score']}"
            )

            linhas.append(
                f"Tendência: {ativo['tendencia']}"
            )

            linhas.append(
                f"RSI: {ativo['rsi']:.1f}"
            )

            linhas.append(
                f"ADX: {ativo['adx']:.1f}"
            )

            linhas.append(
                f"MACD: {ativo['macd_status']}"
            )

            linhas.append(
                f"Stop Loss: {ativo['stop']:.2f}"
            )

            linhas.append(
                f"Recomendação: {ativo['recomendacao']}"
            )

            linhas.append("")

        return "\n".join(linhas)

    def executar(self):

        logger.info(
            "Portfolio Agent iniciado."
        )

        self.analisar()

        dados = self.montar_relatorio()

        resumo = self.gerar_resumo(
            dados
        )

        try:

            relatorio = self.gerar_relatorio_gemini(
                dados
            )

        except Exception:

            logger.exception(
                "Gemini indisponível."
            )

            relatorio = self.gerar_relatorio_local(
                dados
            )

        self.enviar_telegram(
            resumo,
            relatorio
        )

        self.enviar_email(
            relatorio
        )

        self.relatorio.salvar()

        logger.info(
            "Execução finalizada."
        )

def main():

    logger.info(
        "====================================="
    )

    logger.info(
        "Portfolio Agent"
    )

    logger.info(
        "====================================="
    )

    agente = PortfolioAgent()

    agente.executar()

    logger.info(
        "Encerrado com sucesso."
    )
if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.warning(
            "Execução interrompida."
        )

    except Exception:

        logger.exception(
            "Erro fatal."
        )

        raise

##################################### Parte 4 - Metodo executar definitivo ############################

def executar(self):

    logger.info(
        "===================================="
    )

    logger.info(
        "Iniciando Portfolio Agent"
    )

    logger.info(
        "===================================="
    )

    #
    # 1. Análise dos ativos
    #

    self.analisar()

    #
    # 2. Carrega histórico
    #

    anterior = carregar_relatorio_anterior()

    #
    # 3. Monta relatório
    #

    self.relatorio.ativos = self.carteira

    dados = self.relatorio.gerar_json()

    #
    # 4. Comparação
    #

    dados["mudancas"] = comparar(
        dados,
        anterior
    )

    #
    # 5. Resumo Executivo
    #

    resumo = self.gerar_resumo(
        dados
    )

    #
    # 6. Gemini
    #

    try:

        relatorio = analisar_carteira(
            dados
        )

    except Exception:

        logger.exception(
            "Gemini indisponível."
        )

        relatorio = self.gerar_relatorio_local(
            dados
        )

    #
    # 7. Telegram
    #

    self.enviar_telegram(
        resumo,
        relatorio
    )

    #
    # 8. Email
    #

    self.enviar_email(
        relatorio
    )

    #
    # 9. Histórico
    #

    self.relatorio.salvar_json(
        dados
    )

    logger.info(
        "Processo finalizado."
    )
  def main():

    agente = PortfolioAgent()

    agente.executar()
    if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.warning(
            "Execução interrompida."
        )

    except Exception:

        logger.exception(
            "Erro fatal."
        )

        raise
      
