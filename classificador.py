CATEGORIAS = {
    "Receita de Clientes": ["RECEBIMENTO", "PAGAMENTO CLIENTE", "PIX CLIENTE"],
    "Aluguel": ["ALUGUEL"],
    "Contas de Consumo": ["ENERGIA", "INTERNET", "AGUA"],
    "Materiais": ["MATERIAL"],
    "Folha de Pagamento": ["FOLHA", "SALARIO"],
    "Transporte": ["ESTACIONAMENTO", "VEICULO", "COMBUSTIVEL"],
    "Tecnologia": ["EQUIPAMENTOS TI", "CLOUD", "SOFTWARE"],
}

SEM_CATEGORIA = "Não classificado"


def classificar(descricao):
    """Retorna a primeira categoria que tiver uma palavra-chave presente na descrição."""
    descricao = descricao.upper()

    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in descricao:
                return categoria

    return SEM_CATEGORIA
