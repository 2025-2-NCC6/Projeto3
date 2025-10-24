from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Conexão com o DB
load_dotenv()

usuario = os.getenv("usuario")
senha = os.getenv("senha")
host = os.getenv("host")
porta = os.getenv("porta")
banco = os.getenv("banco")

engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{banco}')

Base = declarative_base()

# Definindo a tabela como classe
class mensagens(Base):
    __tablename__ = 'mensagens'

    ID_Mensagem = Column(Integer, primary_key=True, autoincrement=True)
    Mensagem = Column(String(200))
    IP_Cliente = Column(String(15))
    Porta_Cliente = Column(Integer)

class sensores(Base):
    __tablename__ = 'sensores'

    ID_Mensagem = Column(Integer, primary_key=True, autoincrement=True)
    Sensor = Column(String(200))
    IP_Cliente = Column(String(15))
    Dados = Column(String(200))

# Criar a tabela no banco se não existir
Base.metadata.create_all(engine)

# Criar sessão
Session = sessionmaker(bind=engine)
session = Session()

session.commit()
session.close()