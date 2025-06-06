from sqlalchemy import (
    Column, Integer, String, Date, Numeric, Text, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker
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

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'database', 'db.sqlite3')}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)