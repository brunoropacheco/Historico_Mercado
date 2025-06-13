"""
Script para inicializar o banco de dados, criando todas as tabelas conforme os models definidos.
Execute este script uma vez para criar as tabelas no banco de dados.
"""
import os
import sys

# Adicionar o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.database import Base, engine
from src.models.compra import Compra
from src.models.item_compra import ItemCompra

def init_db():
    """Inicializa o banco de dados criando todas as tabelas definidas"""
    Base.metadata.create_all(bind=engine)
    print("Banco de dados inicializado com sucesso.")

if __name__ == "__main__":
    init_db()