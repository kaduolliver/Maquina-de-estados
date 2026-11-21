# Máquina de estados - Ciclo de pedido digital

Exemplo acadêmico para a disciplina **Análise de Algoritmos**.

## Modelo

- Estados: `CRIADO`, `AGUARDANDO_PAGAMENTO`, `EM_PREPARACAO`, `ENVIADO`, `ENTREGUE`, `CANCELADO`.
- Sete transições válidas; `ENTREGUE` e `CANCELADO` são estados terminais.
- Quatro caminhos básicos estruturalmente independentes no grafo com saída única artificial.
- Eventos não permitidos lançam `TransicaoInvalida` e preservam o estado e o histórico.

## Execução

Necessário Python 3.9 ou superior. Não há dependências externas.

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Resultados esperados: **21 testes automatizados**, com validação explícita dos **6/6 estados**, **7/7 transições**, **4/4 caminhos básicos**, além de quatro testes de robustez. O percentual descreve a **cobertura do modelo especificado**, e não mede automaticamente a cobertura de linhas ou ramos de código.

## Arquivos

- `maquina_estados.py`: implementação da máquina e função parcial de transição.
- `tests/test_maquina_estados.py`: testes automatizados em `unittest`.

## Limites do exemplo

Não há integração com meios de pagamento, gestão de estoque, devolução, estorno nem serviços externos. A falha de pagamento mantém o pedido no mesmo estado, permitindo nova tentativa; após confirmação, o cancelamento não é disponibilizado neste modelo didático.
