from ofxparse import OfxParser

from classificador import classificar


def ler_extrato(arquivo):
    """Lê um arquivo OFX (aberto em modo binário) e retorna a lista de movimentações."""
    ofx = OfxParser.parse(arquivo)

    movimentacoes = []
    for transacao in ofx.account.statement.transactions:
        descricao = transacao.memo or transacao.payee

        movimentacoes.append({
            "fitid": transacao.id,
            "data": transacao.date.date(),
            "valor": transacao.amount,
            "descricao": descricao,
            "categoria": classificar(descricao),
        })

    return movimentacoes


def calcular_totais(movimentacoes):
    entradas = 0
    saidas = 0

    for movimentacao in movimentacoes:
        if movimentacao["valor"] > 0:
            entradas += movimentacao["valor"]
        else:
            saidas += movimentacao["valor"]

    saldo = entradas + saidas
    return entradas, saidas, saldo


def totalizar_por_categoria(movimentacoes):
    totais = {}

    for movimentacao in movimentacoes:
        categoria = movimentacao["categoria"]
        totais[categoria] = totais.get(categoria, 0) + movimentacao["valor"]

    return totais
