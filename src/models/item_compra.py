from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Text, create_engine, or_, func
)
from sqlalchemy.orm import declarative_base, sessionmaker, joinedload
import os

# Importar o modelo Compra para junção (join)
from src.models.compra import Compra

Base = declarative_base()

class ItemCompra(Base):
    __tablename__ = 'itens_compra'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(200), nullable=False)
    codigo = Column(String(14), nullable=False)
    unidade = Column(String(14), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    preco_total = Column(Numeric(10, 2), nullable=False)
    compra_id = Column(Integer, nullable=False)  # Chave estrangeira para Compra
    
    def salvar(self):
        """Salva a instância atual no banco de dados"""
        session = SessionLocal()        
        try:
            session.add(self)
            session.commit()
            session.refresh(self)  # Para pegar o id gerado
            return self
        finally:
            session.close()
    
    @classmethod
    def criar(cls, dados):
        """Método de classe para criar e salvar um novo item de compra"""
        item = cls(
            descricao=dados['descricao'],
            codigo=dados['codigo'],
            unidade=dados['unidade'],
            quantidade=dados['quantidade'],
            preco_unitario=dados['preco_unitario'],
            preco_total=dados['preco_total'],
            compra_id=dados['compra_id'],
        )
        return item.salvar()

    @classmethod
    def buscar_por_termo(cls, termo, limit=50, offset=0):
        """
        Busca itens de compra que contenham o termo na descrição.
        
        Args:
            termo (str): Termo a ser buscado na descrição dos itens
            limit (int): Número máximo de resultados
            offset (int): Quantidade de resultados para pular (paginação)
            
        Returns:
            list: Lista de dicionários com os itens e suas informações de compra
        """
        session = SessionLocal()
        try:
            # Preparar o termo de pesquisa para usar com LIKE
            termo_busca = f"%{termo}%"
            
            # Realizar a consulta com join na tabela Compra
            query = session.query(cls, Compra)\
                .join(Compra, cls.compra_id == Compra.id)\
                .filter(cls.descricao.like(termo_busca))\
                .order_by(Compra.data.desc())\
                .limit(limit).offset(offset)
            
            resultados = query.all()
            
            # Formatar resultados
            itens = []
            for item, compra in resultados:
                itens.append({
                    'id': item.id,
                    'descricao': item.descricao,
                    'preco_unitario': float(item.preco_unitario),  # Converter Decimal para float para JSON
                    'quantidade': float(item.quantidade),
                    'unidade': item.unidade,
                    'data_compra': compra.data.strftime('%d/%m/%Y') if compra.data else None,
                    'estabelecimento': compra.estabelecimento,
                    'compra_id': compra.id
                })
            
            return itens
        finally:
            session.close()

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database', 'db.sqlite3')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)