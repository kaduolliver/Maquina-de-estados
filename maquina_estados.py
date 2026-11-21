"""Máquina de estados determinística para o ciclo de um pedido digital.

O modelo é deliberadamente reduzido: não implementa pagamento real,
estorno, estoque nem integração com transportadoras.
"""

from enum import Enum
from typing import List, Tuple


class Estado(str, Enum):
    CRIADO = "CRIADO"
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    EM_PREPARACAO = "EM_PREPARACAO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Evento(str, Enum):
    SOLICITAR_PAGAMENTO = "SOLICITAR_PAGAMENTO"
    CANCELAR = "CANCELAR"
    CONFIRMAR_PAGAMENTO = "CONFIRMAR_PAGAMENTO"
    FALHA_PAGAMENTO = "FALHA_PAGAMENTO"
    DESPACHAR = "DESPACHAR"
    CONFIRMAR_ENTREGA = "CONFIRMAR_ENTREGA"


class TransicaoInvalida(ValueError):
    """O evento recebido não está habilitado no estado atual."""


# Função de transição parcial δ: Estado × Evento -> Estado.
TRANSICOES = {
    (Estado.CRIADO, Evento.SOLICITAR_PAGAMENTO): Estado.AGUARDANDO_PAGAMENTO,
    (Estado.CRIADO, Evento.CANCELAR): Estado.CANCELADO,
    (Estado.AGUARDANDO_PAGAMENTO, Evento.CONFIRMAR_PAGAMENTO): Estado.EM_PREPARACAO,
    (Estado.AGUARDANDO_PAGAMENTO, Evento.CANCELAR): Estado.CANCELADO,
    (Estado.AGUARDANDO_PAGAMENTO, Evento.FALHA_PAGAMENTO): Estado.AGUARDANDO_PAGAMENTO,
    (Estado.EM_PREPARACAO, Evento.DESPACHAR): Estado.ENVIADO,
    (Estado.ENVIADO, Evento.CONFIRMAR_ENTREGA): Estado.ENTREGUE,
}

ESTADOS_TERMINAIS = frozenset({Estado.ENTREGUE, Estado.CANCELADO})
Historico = Tuple[Estado, Evento, Estado]


class MaquinaPedido:
    def __init__(self) -> None:
        self.estado = Estado.CRIADO
        self.historico: List[Historico] = []

    @property
    def finalizado(self) -> bool:
        return self.estado in ESTADOS_TERMINAIS

    def aplicar(self, evento: Evento) -> Estado:
        chave = (self.estado, evento)
        if chave not in TRANSICOES:
            raise TransicaoInvalida(
                f"Evento {evento!r} não permitido no estado {self.estado.value}"
            )
        origem = self.estado
        destino = TRANSICOES[chave]
        self.estado = destino
        self.historico.append((origem, evento, destino))
        return destino
