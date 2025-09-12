import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import database
import logging

# IP e porta do servidor
IP_LOCAL = os.getenv("ip")
PORTA_LOCAL = int(os.getenv("porta_server"))

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("servidor.log"), logging.StreamHandler()]
)

# IP e porta do cliente
ipCliente = None
portaCliente = None

# Bindando o IP e porta do servidor no comando do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_LOCAL, PORTA_LOCAL))
logging.info(f"Servidor iniciado em {IP_LOCAL}:{PORTA_LOCAL}")

# Conexão com o DB
load_dotenv()

usuario = os.getenv("usuario")
senha = os.getenv("senha")
host = os.getenv("host")
porta = os.getenv("porta")
banco = os.getenv("banco")

engine = create_engine(
    f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{banco}',
    pool_pre_ping=True, pool_recycle=3600
)

# Loop para ficar escutando no IP e porta local
while True:
    try:
        # data = mensagem recebida || addr = IP e porta do cliente
        data, addr = sock.recvfrom(1024)

        # Designando o endereço do cliente
        ipCliente = addr[0]
        portaCliente = addr[1]

        # Enviando informacoes para o banco de dados
        nova_mensagem = database.mensagens(
        Mensagem = data.decode('utf-8'),
        IP_Cliente = ipCliente,
        Porta_Cliente = portaCliente
        )

        Session = sessionmaker(bind=engine)
        session = Session()

        session.add(nova_mensagem)
        session.commit()
        session.close()

        # Imprimindo a mensagem e IP e porta do cliente no console
        logging.info(f"Mensagem recebida: {data.decode('utf-8')} de {ipCliente}:{portaCliente}")

        # Retornando resposta de recebimento para cliente
        sock.sendto(b"ACK", (ipCliente, portaCliente))
        
    except Exception as e:
        logging.error(f"Erro no servidor: {e}")
