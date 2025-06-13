import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carrega variáveis de ambiente para conexão Railway PostgreSQL
PGUSER = os.environ.get("POSTGRES_USER")
PGPASSWORD = os.environ.get("POSTGRES_PASSWORD")
PGDATABASE = os.environ.get("POSTGRES_DB")
PGHOST = os.environ.get("RAILWAY_TCP_PROXY_DOMAIN")
PGPORT = os.environ.get("RAILWAY_TCP_PROXY_PORT")

# Verifica se todas as variáveis necessárias para PostgreSQL estão presentes
if not all([PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE]):
    missing_vars = []
    if not PGUSER: missing_vars.append("POSTGRES_USER")
    if not PGPASSWORD: missing_vars.append("POSTGRES_PASSWORD")
    if not PGDATABASE: missing_vars.append("POSTGRES_DB")
    if not PGHOST: missing_vars.append("RAILWAY_TCP_PROXY_DOMAIN")
    if not PGPORT: missing_vars.append("RAILWAY_TCP_PROXY_PORT")
    
    error_message = f"Erro de configuração: As seguintes variáveis de ambiente são obrigatórias: {', '.join(missing_vars)}"
    raise EnvironmentError(error_message)

# Configura a URL do banco de dados PostgreSQL
DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
print(f"Conectando ao PostgreSQL: {PGHOST}:{PGPORT}/{PGDATABASE}")

# Configuração do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()