from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AtivoConfig:
    """Configuração estática de um ativo da carteira."""

    ticker: str
    nome: str
    classe: str
    pais: str
    moeda: str
    setor: str
