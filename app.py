import streamlit as st

from banco import salvar_movimentacoes
from leitor_ofx import calcular_totais, ler_extrato, totalizar_por_categoria

st.title("Importação de Extrato OFX")

arquivo = st.file_uploader("Selecione o arquivo OFX", type=["ofx"])

if arquivo:
    try:
        movimentacoes = ler_extrato(arquivo)
    except Exception:
        st.error("Não foi possível ler o arquivo. Verifique se é um OFX válido.")
        st.stop()

    novas = salvar_movimentacoes(movimentacoes)
    st.success(f"{novas} novas movimentações gravadas no banco.")

    entradas, saidas, saldo = calcular_totais(movimentacoes)
    coluna1, coluna2, coluna3 = st.columns(3)
    coluna1.metric("Entradas", f"R$ {entradas:.2f}")
    coluna2.metric("Saídas", f"R$ {saidas:.2f}")
    coluna3.metric("Saldo", f"R$ {saldo:.2f}")

    st.subheader("Total por categoria")
    totais = totalizar_por_categoria(movimentacoes)
    # O gráfico não entende o tipo Decimal, por isso convertemos para float
    st.bar_chart({categoria: float(total) for categoria, total in totais.items()})

    st.subheader(f"Movimentações ({len(movimentacoes)})")
    st.dataframe(movimentacoes)
