from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Text, create_engine, func, desc, between
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import os

Base = declarative_base()

class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, default=datetime.date.today, nullable=False)
    estabelecimento = Column(String(200), nullable=False)
    cnpj = Column(String(14), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    
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
        """Método de classe para criar e salvar uma nova compra"""
        compra = cls(
            data=dados['data'],
            estabelecimento=dados['estabelecimento'],
            cnpj=dados['cnpj'],
            total=dados['total'],
        )
        return compra.salvar()
    
    @classmethod
    def buscar_por_estabelecimento(cls, estabelecimento, limit=50, offset=0):
        """Busca compras por nome do estabelecimento"""
        session = SessionLocal()
        try:
            termo_busca = f"%{estabelecimento}%"
            query = session.query(cls)\
                .filter(cls.estabelecimento.like(termo_busca))\
                .order_by(cls.data.desc())\
                .limit(limit).offset(offset)
            return query.all()
        finally:
            session.close()
    
    @classmethod
    def buscar_por_periodo(cls, data_inicio, data_fim, limit=50, offset=0):
        """Busca compras realizadas dentro de um período específico"""
        session = SessionLocal()
        try:
            query = session.query(cls)\
                .filter(cls.data.between(data_inicio, data_fim))\
                .order_by(cls.data.desc())\
                .limit(limit).offset(offset)
            return query.all()
        finally:
            session.close()
    
    @classmethod
    def obter_itens(cls, compra_id):
        """Obtém todos os itens associados a uma compra específica"""
        from src.models.item_compra import ItemCompra  # Importação local para evitar circular import
        
        session = SessionLocal()
        try:
            query = session.query(ItemCompra)\
                .filter(ItemCompra.compra_id == compra_id)\
                .order_by(ItemCompra.id)
            return query.all()
        finally:
            session.close()
    
    @classmethod
    def buscar_por_id(cls, compra_id):
        """
        Busca uma compra específica pelo seu ID.
        
        Args:
            compra_id (int): O ID da compra a ser buscada
            
        Returns:
            Compra: A instância da compra encontrada ou None se não existir
        """
        session = SessionLocal()
        try:
            return session.query(cls).filter(cls.id == compra_id).first()
        finally:
            session.close()
    
    @classmethod
    def buscar_compras_recentes(cls, limit=10):
        """Retorna as compras mais recentes."""
        session = SessionLocal()
        try:
            return session.query(cls).order_by(cls.data.desc()).limit(limit).all()
        finally:
            session.close()

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database', 'db.sqlite3')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)