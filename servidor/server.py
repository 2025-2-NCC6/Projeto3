import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import database

# IP e porta do servidor
IP_LOCAL = "127.0.0.1"
PORTA_LOCAL = 5005

# Mensagem de retorno
RESPOSTA = b"ok"

# IP e porta do cliente
ipCliente = None
portaCliente = None

# Bindando o IP e porta do servidor no comando do socket
sock = socket.socket(socket.AF_INET, # IPv4
                     socket.SOCK_DGRAM) # Socket UDP
sock.bind((IP_LOCAL, PORTA_LOCAL))

# Conexão com o DB
load_dotenv()

usuario = os.getenv("usuario")
senha = os.getenv("senha")
host = os.getenv("host")
porta = os.getenv("porta")
banco = os.getenv("banco")

engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{banco}')

# Loop para ficar escutando no IP e porta local
while True:
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
    print(f"\nMensagem recebida: {data.decode('utf-8')}")
    print(f"\nMensagem de\nIP: {ipCliente}\nPORT: {portaCliente}")

    # Retornando resposta de recebimento para cliente
    if(ipCliente != None or portaCliente != None):
        sock.sendto(RESPOSTA, (ipCliente, portaCliente))