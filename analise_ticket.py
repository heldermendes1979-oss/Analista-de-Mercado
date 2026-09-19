"""
analise_ticket.py
-----------------

Programa principal do Portfolio Agent.

Fluxo:

1. Carrega configurações
2. Analisa todos os ativos
3. Calcula score
4. Gera relatório estruturado
5. Envia ao Gemini
6. Envia Telegram
7. Envia e-mail
8. Salva histórico
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

from colorlog import ColoredFormatter

from config import CARTEIRA, Config
from email_sender import enviar_relatorio as enviar_email
from gemini import analisar_carteira
from indicadores import analisar_ativo
from relatorio import Relatorio, comparar, carregar_relatorio_anterior
from score import ScoreTecnico
from telegram_sender import enviar_relatorio, enviar_resumo


def _configurar_logger() -> logging.Logger:
    """Configura o logger do módulo apenas uma vez."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    LOG_DIR = Path(Config.LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    formatter_colorido = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(message)s"
    )
    formatter_arquivo = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    )

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter_colorido)

    arquivo = logging.FileHandler(
        LOG_DIR / "portfolio.log",
        encoding="utf-8",
    )
    arquivo.setFormatter(formatter_arquivo)

    logger.addHandler(console)
    logger.addHandler(arquivo)
    logger.propagate = False
    return logger


logger = _configurar_logger()


def _obter_dados_ativo(item: Any) -> dict[str, str]:
    """
    Aceita tanto dicionário quanto objeto com atributos
    e retorna os metadados do ativo em formato uniforme.
    """
    if isinstance(item, dict):
        return {
            "ticker": item.get("ticker", ""),
            "nome": item.get("nome", ""),
            "classe": item.get("classe", ""),
            "pais": item.get("pais", ""),
            "moeda": item.get("moeda", ""),
            "setor": item.get("setor", ""),
        }

    return {
        "ticker": getattr(item, "ticker", ""),
        "nome": getattr(item, "nome", ""),
        "classe": getattr(item, "classe", ""),
        "pais": getattr(item, "pais", ""),
        "moeda": getattr(item, "moeda", ""),
        "setor": getattr(item, "setor", ""),
    }


def _acao_resumida(recomendacao: str) -> str:
    """Converte a recomendação técnica em uma ação curta."""
    texto = (recomendacao or "").lower()

    if "compra forte" in texto:
        return "Aumentar posição"
    if "compra" in texto:
        return "Comprar"
    if "manter" in texto:
        return "Manter"
    if "reduzir" in texto:
        return "Reduzir"
    return "Vender"


def _justificativa_curta(ativo: dict[str, Any]) -> str:
    """Gera uma justificativa curta e direta para o ativo."""
    score = int(ativo.get("score", 0))
    tendencia = str(ativo.get("tendencia", "")).lower()
    rsi = float(ativo.get("rsi", 0) or 0)
    macd_status = str(ativo.get("macd_status", "")).lower()
    volume_status = str(ativo.get("volume_status", "")).lower()

    if score >= 90:
        return "Tendência forte, momento positivo e risco controlado."
    if score >= 80:
        return "Configuração favorável e boa relação risco-retorno."
    if score >= 65:
        return "Sinal neutro/positivo; manter posição."
    if score >= 45:
        return "Sinais mistos; reduzir exposição."
    if "baixa" in tendencia or rsi < 35:
        return "Tendência fraca e sinais técnicos desfavoráveis."
    if "compra" in macd_status or "acima" in volume_status:
        return "Momento melhora, mas ainda com cautela."
    return "Sem força técnica suficiente para compra."
   
class PortfolioAgent:
    """Orquestra a análise técnica, o relatório e os envios."""

    def __init__(self) -> None:
        self.carteira = []
        self.relatorio = Relatorio()
        
    """Orquestra a análise técnica, o relatório e os envios."""

    def __init__(self) -> None:
        self.carteira: list[Any] = []
        self.relatorio = Relatorio()

    def analisar(self) -> None:
        """Executa a análise técnica de todos os ativos da carteira."""
        logger.info("Iniciando análise da carteira...")

        self.carteira = []

        for item in CARTEIRA:
            dados = _obter_dados_ativo(item)
            ticker = dados["ticker"]

            try:
                logger.info("Analisando %s", ticker)

                ativo = analisar_ativo(ticker)
                ativo.nome = dados["nome"]
                ativo.classe = dados["classe"]
                ativo.pais = dados["pais"]
                ativo.moeda = dados["moeda"]
                ativo.setor = dados["setor"]

                ScoreTecnico.calcular(ativo)
                self.carteira.append(ativo)

            except Exception:
                logger.exception("Erro ao processar %s", ticker)

        logger.info("Carteira analisada.")

    def montar_relatorio(self) -> dict[str, Any]:
        """Gera o relatório estruturado e adiciona as mudanças em relação à execução anterior."""
        anterior = carregar_relatorio_anterior()

        self.relatorio.ativos = list(self.carteira)
        atual = self.relatorio.gerar_json()
        atual["mudancas"] = comparar(atual, anterior)

        return atual

    def salvar_historico(self, dados: dict[str, Any]) -> None:
        """Salva o relatório atual em disco para comparação futura."""
        Path(Config.DATA_DIR).mkdir(parents=True, exist_ok=True)

        arquivo = Path(Config.HISTORICO_FILE)
        arquivo.parent.mkdir(parents=True, exist_ok=True)

        with arquivo.open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def gerar_resumo(self, dados: dict[str, Any]) -> str:
        """Gera um resumo curto, direto e orientado à ação."""
        estat = dados.get("estatisticas", {})
        ativos = dados.get("ativos", [])

        melhores = ativos[:3]
        piores = ativos[-2:] if len(ativos) >= 2 else ativos

        linhas: list[str] = []
        linhas.append("RESUMO EXECUTIVO")
        linhas.append("")
        linhas.append(f"Data: {dados.get('data', '')}")
        linhas.append(f"Ativos analisados: {estat.get('total_ativos', 0)}")
        linhas.append(f"Score médio: {estat.get('score_medio', 0)}")
        linhas.append("")
        linhas.append("AÇÕES PRIORITÁRIAS")
        linhas.append("")

        for ativo in melhores:
            ticker = ativo.get("ticker", "")
            acao = _acao_resumida(str(ativo.get("recomendacao", "")))
            justificativa = _justificativa_curta(ativo)
            linhas.append(f"- {ticker}: {acao} | {justificativa}")

        linhas.append("")
        linhas.append("ATIVOS QUE EXIGEM ATENÇÃO")
        linhas.append("")

        for ativo in piores:
            ticker = ativo.get("ticker", "")
            acao = _acao_resumida(str(ativo.get("recomendacao", "")))
            justificativa = _justificativa_curta(ativo)
            linhas.append(f"- {ticker}: {acao} | {justificativa}")

        return "\n".join(linhas)
            def gerar_relatorio_gemini(self, dados: dict[str, Any]) -> str:
        """Solicita ao Gemini um relatório textual a partir do JSON da carteira."""
        logger.info("Solicitando análise ao Gemini...")
        return analisar_carteira(dados)

    def gerar_relatorio_local(self, dados: dict[str, Any]) -> str:
        """Gera um relatório local simples caso o Gemini falhe."""
        linhas: list[str] = []
        linhas.append("RELATÓRIO TÉCNICO")
        linhas.append("")
        linhas.append(f"Data: {dados.get('data', '')}")
        linhas.append("")

        for ativo in dados.get("ativos", []):
            ticker = ativo.get("ticker", "")
            acao = _acao_resumida(str(ativo.get("recomendacao", "")))
            justificativa = _justificativa_curta(ativo)
            score = ativo.get("score", 0)
            preco = ativo.get("preco", 0)

            linhas.append(f"- {ticker}: {acao}")
            linhas.append(f"  Preço: {preco}")
            linhas.append(f"  Score: {score}")
            linhas.append(f"  Justificativa: {justificativa}")
            linhas.append("")

        return "\n".join(linhas)

    def enviar_telegram(self, resumo: str, relatorio: str) -> None:
        """Envia o resumo e o relatório completo para o Telegram."""
        logger.info("Enviando Telegram...")

        try:
            enviar_resumo(resumo)
            enviar_relatorio(relatorio)
            logger.info("Telegram enviado.")
        except Exception:
            logger.exception("Erro no envio ao Telegram.")

    def enviar_email(self, relatorio: str) -> None:
        """Envia o relatório por e-mail."""
        logger.info("Enviando e-mail...")

        try:
            enviar_email(relatorio)
            logger.info("E-mail enviado.")
        except Exception:
            logger.exception("Erro no envio do e-mail.")

    def executar(self) -> None:
        """Executa o fluxo completo da análise."""
        logger.info("Portfolio Agent iniciado.")

        self.analisar()
        dados = self.montar_relatorio()
        resumo = self.gerar_resumo(dados)

        try:
            relatorio = self.gerar_relatorio_gemini(dados)
        except Exception:
            logger.exception("Gemini indisponível.")
            relatorio = self.gerar_relatorio_local(dados)

        self.enviar_telegram(resumo, relatorio)
        self.enviar_email(relatorio)
        self.salvar_historico(dados)

        logger.info("Processo finalizado.")
        def main() -> None:
    """Ponto de entrada do programa."""
    agente = PortfolioAgent()
    agente.executar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Execução interrompida.")
    except Exception:
        logger.exception("Erro fatal.")
        raise
