"""
Controller responsável por processar os dados extraídos das notas fiscais
e inserir as informações no banco de dados, utilizando os models de Compra e ItensCompra.
"""

from src.models.compra import Compra
#from src.models.itens_compra import ItensCompra

def salvar_dados_nota(dados_nota):
    """
    Recebe um dicionário com os dados extraídos da nota fiscal e salva no banco de dados.
    Espera um formato como:
    {
        'estabelecimento': ...,
        'cnpj': ...,
        'data': ...,
        'total': ...,
        'itens': [
            {'descricao': ..., 'quantidade': ..., 'unidade': ..., 'preco_unitario': ..., 'preco_total': ...},
            ...
        ]
    }
    """
    print('\n\n\n')
    print('Salvando dados da nota:', dados_nota)
           # Cria e salva a compra
    compra = Compra(
        estabelecimento=dados_nota.get('nome_empresa'),
        cnpj=dados_nota.get('cnpj'),
        data=dados_nota.get('data'),
        total=dados_nota.get('total')
    )
    compra.salvar()  # Método do model Compra para inserir no banco
    '''
    # Salva os itens da compra
    for item in dados_nota.get('itens', []):
        item_compra = ItensCompra(
            compra_id=compra.id,  # Supondo que o model gera o id ao salvar
            descricao=item.get('descricao'),
            quantidade=item.get('quantidade'),
            unidade=item.get('unidade'),
            preco_unitario=item.get('preco_unitario'),
            preco_total=item.get('preco_total')
        )
        item_compra.salvar()  # Método do model ItensCompra para inserir no banco
    '''
    return compra.id  # Retorna o id da compra salva