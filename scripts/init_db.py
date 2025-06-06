"""
Script para inicializar o banco de dados, criando todas as tabelas conforme os models definidos.
Execute este script uma vez para criar as tabelas no banco de dados.
"""
import os
import sys

def init_db():
    # Adiciona a pasta raiz do projeto (um nível acima da pasta 'scripts') ao sys.path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Cria os diretórios para o banco de dados se não existirem
    db_dir = os.path.join(project_root, 'data', 'database')
    os.makedirs(db_dir, exist_ok=True)
    print(f"Diretório do banco de dados criado/verificado: {db_dir}")
    
    # Caminho completo do arquivo do banco de dados
    db_path = os.path.join(db_dir, 'db.sqlite3')
    
    # Verificar se o banco já existe
    if os.path.exists(db_path):
        print(f"Banco de dados existente encontrado: {db_path}")
        print("As tabelas serão atualizadas se necessário.")
    else:
        print(f"Novo banco de dados será criado: {db_path}")
        # Cria o arquivo vazio do banco de dados
        with open(db_path, 'w'):
            pass
    
    # Importa os models após definir o sys.path
    from src.models.compra import Base as CompraBase, engine as compra_engine
    
    # Cria as tabelas de cada model
    print("Criando tabela 'compras'...")
    CompraBase.metadata.create_all(bind=compra_engine)
    
    print("Criando tabela 'itens_compra'...")
    # Descomente e ajuste quando tiver o model de itens_compra
    # from src.models.itens_compra import Base as ItensCompraBase, engine as itens_compra_engine
    # ItensCompraBase.metadata.create_all(bind=itens_compra_engine)
    
    # Verificar se o arquivo foi criado com sucesso
    if os.path.exists(db_path):
        print(f"Banco de dados inicializado com sucesso em: {db_path}")
    else:
        print(f"ERRO: Falha ao criar o arquivo do banco de dados em: {db_path}")

if __name__ == "__main__":
    init_db()