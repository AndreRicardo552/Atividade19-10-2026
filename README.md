# Leitura de Arquivos OFX com Python

Aplicação que lê um extrato bancário no formato **OFX**, exibe as movimentações, classifica cada uma em uma categoria e grava tudo em um banco **PostgreSQL**, sem duplicar registros.

É um exemplo simples de **ETL**:
- **Extração:** leitura do arquivo OFX
- **Transformação:** organização dos dados e classificação por categoria
- **Carga:** gravação no PostgreSQL

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Programa principal pelo terminal |
| `app.py` | Tela de upload com Streamlit |
| `leitor_ofx.py` | Lê o OFX e calcula os totais |
| `classificador.py` | Define a categoria pela descrição |
| `banco.py` | Conexão e gravação no PostgreSQL |
| `criar_tabela.sql` | Criação da tabela `movimentacoes` |

## Como rodar

### 1. Ambiente

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Banco de dados

1. Com o PostgreSQL instalado, criar o banco `extrato_ofx` (pelo DBeaver ou `CREATE DATABASE extrato_ofx;`).
2. Executar o `criar_tabela.sql` nesse banco.
3. Copiar `.env.example` para `.env` e preencher a senha do PostgreSQL.

### 3. Executar

Pelo terminal:

```
python main.py
```

Pela tela de upload:

```
streamlit run app.py
```

## Saída do `extrato.ofx` de exemplo

```
Total de movimentações: 15
Entradas: R$ 17900.00
Saídas:   R$ -6059.70
Saldo:    R$ 11840.30

TOTAL POR CATEGORIA
Receita de Clientes    R$   17900.00
Aluguel                R$    -850.00
Contas de Consumo      R$    -519.80
Materiais              R$    -760.00
Folha de Pagamento     R$   -2100.00
Transporte             R$    -790.00
Tecnologia             R$   -1039.90

15 novas movimentações gravadas no banco.
```

Rodando de novo, nenhuma movimentação é duplicada:

```
0 novas movimentações gravadas no banco.
```

## Como não duplica

Cada transação do OFX tem um código único (`FITID`). A coluna `fitid` da tabela é `UNIQUE`, e o `INSERT` usa `ON CONFLICT (fitid) DO NOTHING`, então transações já gravadas são ignoradas.

## Como classifica

O `classificador.py` tem um dicionário de categorias com palavras-chave. A primeira categoria que tiver uma palavra presente na descrição é a escolhida; se nenhuma tiver, a movimentação fica como "Não classificado". Para criar uma categoria nova, basta adicionar uma linha no dicionário.

## Observação sobre o saldo

O saldo calculado (R$ 11.840,30) é diferente do saldo final informado no arquivo (R$ 12.030,20) porque o OFX não traz o saldo inicial da conta.
