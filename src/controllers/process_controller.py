"""
Controller responsável por processar os dados extraídos das notas fiscais
e inserir as informações no banco de dados, utilizando os models de Compra e ItensCompra.
"""

from src.models.compra import Compra
from src.models.item_compra import ItemCompra

def salvar_dados_nota(dados_nota):
    """
    Recebe um dicionário com os dados extraídos da nota fiscal e salva no banco de dados.
    """
    print('\n\n\n')
    print('Salvando dados da compra:', dados_nota)
           # Cria e salva a compra
    compra = Compra(
        estabelecimento=dados_nota.get('nome_empresa'),
        cnpj=dados_nota.get('cnpj'),
        data=dados_nota.get('data'),
        total=dados_nota.get('total')
    )
    compra.salvar()  # Método do model Compra para inserir no banco
    print('Dentro de process_controlles Compra salva com sucesso. partindo para itens_compra')
    
    # Salva os itens da compra
    print(dados_nota.get('itens_compra', []))
    print(dados_nota.get('itens_compra'))
    for item in dados_nota.get('itens_compra', []):
        print('\n\n\n')
        print('Salvando item da compra:', item)
        # Converte strings com vírgula para float com duas casas decimais
        preco_unitario = float(str(item.get('valor_unitario')).replace(',', '.'))
        preco_total = float(str(item.get('valor_total')).replace(',', '.'))
        item_compra = ItemCompra(
            compra_id=compra.id,  # Supondo que o model gera o id ao salvar
            descricao=item.get('descricao'),
            codigo=item.get('codigo'),
            quantidade=item.get('quantidade'),
            unidade=item.get('unidade'),
            preco_unitario=round(preco_unitario, 2),
            preco_total=round(preco_total, 2)
        )
        item_compra.salvar()  # Método do model ItemCompra para inserir no banco
    
    return compra.id  # Retorna o id da compra salva