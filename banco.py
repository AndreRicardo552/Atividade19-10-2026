import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def salvar_movimentacoes(movimentacoes):
    """Grava as movimentações no banco e retorna quantas eram novas.

    Movimentações com um FITID já gravado são ignoradas.
    """
    novas = 0

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            for movimentacao in movimentacoes:
                cursor.execute(
                    """
                    INSERT INTO movimentacoes
                        (data_movimentacao, valor, descricao, fitid, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (fitid) DO NOTHING
                    """,
                    (
                        movimentacao["data"],
                        movimentacao["valor"],
                        movimentacao["descricao"],
                        movimentacao["fitid"],
                        movimentacao["categoria"],
                    ),
                )
                novas += cursor.rowcount  # 1 se gravou, 0 se já existia

    conexao.close()
    return novas
