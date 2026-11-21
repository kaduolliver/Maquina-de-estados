"""Testes inteiramente automatizados: estados, transições, caminhos e erros."""

import unittest

from maquina_estados import Estado, Evento, MaquinaPedido, TransicaoInvalida, TRANSICOES


C = Evento.CANCELAR
S = Evento.SOLICITAR_PAGAMENTO
P = Evento.CONFIRMAR_PAGAMENTO
F = Evento.FALHA_PAGAMENTO
D = Evento.DESPACHAR
E = Evento.CONFIRMAR_ENTREGA


def executar(*eventos):
    maquina = MaquinaPedido()
    for evento in eventos:
        maquina.aplicar(evento)
    return maquina


class TesteEstados(unittest.TestCase):
    """Seis estados alcançáveis, cada um validado por uma asserção."""

    def test_estado_criado(self):
        self.assertEqual(executar().estado, Estado.CRIADO)

    def test_estado_aguardando_pagamento(self):
        self.assertEqual(executar(S).estado, Estado.AGUARDANDO_PAGAMENTO)

    def test_estado_em_preparacao(self):
        self.assertEqual(executar(S, P).estado, Estado.EM_PREPARACAO)

    def test_estado_enviado(self):
        self.assertEqual(executar(S, P, D).estado, Estado.ENVIADO)

    def test_estado_entregue(self):
        maquina = executar(S, P, D, E)
        self.assertEqual(maquina.estado, Estado.ENTREGUE)
        self.assertTrue(maquina.finalizado)

    def test_estado_cancelado(self):
        maquina = executar(C)
        self.assertEqual(maquina.estado, Estado.CANCELADO)
        self.assertTrue(maquina.finalizado)


class TesteTransicoes(unittest.TestCase):
    """Sete arestas do grafo, verificadas isoladamente."""

    def conferir(self, prefixo, evento, origem, destino):
        maquina = executar(*prefixo)
        self.assertEqual(maquina.estado, origem)
        self.assertEqual(maquina.aplicar(evento), destino)
        self.assertEqual(maquina.historico[-1], (origem, evento, destino))

    def test_t01_solicitar_pagamento(self):
        self.conferir((), S, Estado.CRIADO, Estado.AGUARDANDO_PAGAMENTO)

    def test_t02_cancelar_pedido_criado(self):
        self.conferir((), C, Estado.CRIADO, Estado.CANCELADO)

    def test_t03_confirmar_pagamento(self):
        self.conferir((S,), P, Estado.AGUARDANDO_PAGAMENTO, Estado.EM_PREPARACAO)

    def test_t04_cancelar_pagamento_pendente(self):
        self.conferir((S,), C, Estado.AGUARDANDO_PAGAMENTO, Estado.CANCELADO)

    def test_t05_falha_de_pagamento(self):
        self.conferir((S,), F, Estado.AGUARDANDO_PAGAMENTO, Estado.AGUARDANDO_PAGAMENTO)

    def test_t06_despachar(self):
        self.conferir((S, P), D, Estado.EM_PREPARACAO, Estado.ENVIADO)

    def test_t07_confirmar_entrega(self):
        self.conferir((S, P, D), E, Estado.ENVIADO, Estado.ENTREGUE)


class TesteCaminhos(unittest.TestCase):
    """Quatro caminhos linearmente independentes na base estrutural."""

    def conferir_caminho(self, eventos, destino):
        maquina = executar(*eventos)
        self.assertEqual(maquina.estado, destino)
        self.assertTrue(maquina.finalizado)
        self.assertEqual([evento for _, evento, _ in maquina.historico], list(eventos))
        self.assertEqual(len(maquina.historico), len(eventos))

    def test_p01_entrega_direta(self):
        self.conferir_caminho((S, P, D, E), Estado.ENTREGUE)

    def test_p02_cancelamento_imediato(self):
        self.conferir_caminho((C,), Estado.CANCELADO)

    def test_p03_cancelamento_aguardando_pagamento(self):
        self.conferir_caminho((S, C), Estado.CANCELADO)

    def test_p04_erro_e_retentativa(self):
        self.conferir_caminho((S, F, P, D, E), Estado.ENTREGUE)


class TesteRobustez(unittest.TestCase):
    """Eventos não permitidos, estados terminais e imutabilidade no erro."""

    def test_evento_invalido_no_estado_inicial(self):
        maquina = MaquinaPedido()
        with self.assertRaises(TransicaoInvalida):
            maquina.aplicar(E)
        self.assertEqual(maquina.estado, Estado.CRIADO)
        self.assertEqual(maquina.historico, [])

    def test_termino_por_entrega_nao_aceita_eventos(self):
        maquina = executar(S, P, D, E)
        historico = list(maquina.historico)
        with self.assertRaises(TransicaoInvalida):
            maquina.aplicar(C)
        self.assertEqual(maquina.estado, Estado.ENTREGUE)
        self.assertEqual(maquina.historico, historico)

    def test_termino_por_cancelamento_nao_aceita_eventos(self):
        maquina = executar(C)
        with self.assertRaises(TransicaoInvalida):
            maquina.aplicar(S)
        self.assertEqual(maquina.estado, Estado.CANCELADO)
        self.assertEqual(len(maquina.historico), 1)

    def test_repetidas_falhas_de_pagamento(self):
        maquina = executar(S, F, F, P)
        self.assertEqual(maquina.estado, Estado.EM_PREPARACAO)
        self.assertEqual(len(maquina.historico), 4)
        self.assertEqual(len(TRANSICOES), 7)


if __name__ == "__main__":
    unittest.main()
