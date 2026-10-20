from banco import salvar_movimentacoes
from leitor_ofx import calcular_totais, ler_extrato, totalizar_por_categoria

ARQUIVO_OFX = "extrato.ofx"


def exibir_movimentacoes(movimentacoes):
    print("EXTRATO BANCÁRIO")

    for movimentacao in movimentacoes:
        print(f"""
Data      : {movimentacao['data'].strftime('%d/%m/%Y')}
Valor     : R$ {movimentacao['valor']:.2f}
Descrição : {movimentacao['descricao']}
Categoria : {movimentacao['categoria']}
--------------------------------------""")


def exibir_resumo(movimentacoes):
    entradas, saidas, saldo = calcular_totais(movimentacoes)

    print(f"\nTotal de movimentações: {len(movimentacoes)}")
    print(f"Entradas: R$ {entradas:.2f}")
    print(f"Saídas:   R$ {saidas:.2f}")
    print(f"Saldo:    R$ {saldo:.2f}")


def exibir_totais_por_categoria(movimentacoes):
    print("\nTOTAL POR CATEGORIA")

    for categoria, total in totalizar_por_categoria(movimentacoes).items():
        print(f"{categoria:<22} R$ {total:>10.2f}")


def main():
    with open(ARQUIVO_OFX, "rb") as arquivo:
        movimentacoes = ler_extrato(arquivo)

    exibir_movimentacoes(movimentacoes)
    exibir_resumo(movimentacoes)
    exibir_totais_por_categoria(movimentacoes)

    novas = salvar_movimentacoes(movimentacoes)
    print(f"\n{novas} novas movimentações gravadas no banco.")


if __name__ == "__main__":
    main()
