"""
Controller responsável por processar os dados extraídos das notas fiscais
e inserir as informações no banco de dados, utilizando os models de Compra e ItensCompra.
"""

from src.models.compra import Compra
from src.models.item_compra import ItemCompra
import logging

# Configuração de logging se ainda não existir
logger = logging.getLogger(__name__)

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

def buscar_itens_por_termo(termo, limit=50, offset=0):
    """
    Busca itens de compra que contenham o termo na descrição.
    
    Args:
        termo (str): Termo a ser buscado na descrição dos itens
        limit (int): Número máximo de resultados
        offset (int): Posição inicial para paginação
        
    Returns:
        list: Lista de resultados formatados com dados do item e da compra
    """
    try:
        # Utiliza o método do modelo ItemCompra para buscar 
        resultados = ItemCompra.buscar_por_termo(termo, limit, offset)
        
        # Formata os resultados para retorno
        itens_formatados = []
        for resultado in resultados:
            itens_formatados.append({
                'id': resultado['id'],
                'descricao': resultado['descricao'],
                'preco_unitario': resultado['preco_unitario'],
                'data_compra': resultado['data_compra'],
                'estabelecimento': resultado['estabelecimento'],
                'unidade': resultado['unidade'],
                'quantidade': resultado['quantidade'],
                'compra_id': resultado['compra_id']
            })
        
        return {
            'success': True,
            'total': len(itens_formatados),
            'itens': itens_formatados
        }
    except Exception as e:
        logger.error(f"Erro ao buscar itens por termo '{termo}': {str(e)}")
        return {
            'success': False,
            'error': f"Erro ao buscar itens: {str(e)}",
            'itens': []
        }

def buscar_compras_recentes(limit=10):
    """
    Retorna as compras mais recentes.
    
    Args:
        limit (int): Número máximo de compras recentes
        
    Returns:
        dict: Dicionário com status e lista das compras mais recentes
    """
    try:
        # Delegar para o modelo Compra
        compras = Compra.buscar_compras_recentes(limit)
        
        resultado = []
        for compra in compras:
            resultado.append({
                'id': compra.id,
                'data': compra.data.strftime('%d/%m/%Y'),
                'estabelecimento': compra.estabelecimento,
                'total': float(compra.total)
            })
        
        return {
            'success': True,
            'total': len(resultado),
            'compras': resultado
        }
    except Exception as e:
        logger.error(f"Erro ao buscar compras recentes: {str(e)}")
        return {
            'success': False,
            'error': f"Erro ao buscar compras recentes: {str(e)}",
            'compras': []
        }

def obter_detalhes_compra(compra_id):
    """
    Obtém os detalhes completos de uma compra, incluindo todos seus itens.
    
    Args:
        compra_id (int): ID da compra a ser consultada
        
    Returns:
        dict: Detalhes da compra e seus itens
    """
    try:
        # Busca a compra
        compra = Compra.buscar_por_id(compra_id)
        if not compra:
            return {
                'success': False,
                'error': f"Compra com ID {compra_id} não encontrada"
            }
            
        # Busca os itens da compra
        itens = ItemCompra.buscar_por_compra_id(compra_id)
        
        # Formata os dados para retorno
        itens_formatados = []
        for item in itens:
            itens_formatados.append({
                'id': item.id,
                'descricao': item.descricao,
                'quantidade': float(item.quantidade),
                'unidade': item.unidade,
                'preco_unitario': float(item.preco_unitario),
                'preco_total': float(item.preco_total)
            })
            
        return {
            'success': True,
            'compra': {
                'id': compra.id,
                'data': compra.data.strftime('%d/%m/%Y'),
                'estabelecimento': compra.estabelecimento,
                'cnpj': compra.cnpj,
                'total': float(compra.total),
                'itens': itens_formatados
            }
        }
    except Exception as e:
        logger.error(f"Erro ao obter detalhes da compra {compra_id}: {str(e)}")
        return {
            'success': False,
            'error': f"Erro ao obter detalhes da compra: {str(e)}"
        }