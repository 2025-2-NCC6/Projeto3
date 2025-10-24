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

# Função para lidar com os requests
def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request_data}")

    log = os.linesep.join([s for s in request_data.splitlines() if s])
    request_lines = request_data.split('\n')

    if request_lines:

        first_line = request_lines[0].split()

        if len(first_line) > 1:
            method = first_line[0]
            path = first_line[1]

            # Rotas do servidor
            if method == 'GET' and path == '/':
                response_body = "<h1>Funcionando</h1>"
                response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
                for i in range(len(request_lines)):
                    logging.info(f"Received request:\n{request_lines[i]}")
            elif method == 'GET' and path == '/teste':
                response_body = "<h1>TESTE</h1>"
                response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
                for i in range(len(request_lines)):
                    logging.info(f"Received request:\n{request_lines[i]}")
            else:
                response_body = "<h1>404 Not Found</h1>"
                response_headers = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n"
                response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
                logging.error("404 Not Found")

        else:
            response_body = "<h1>400 Bad Request</h1>"
            response_headers = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
            response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
            logging.error("400 Bad Request")
    else:
        response_body = "<h1>400 Bad Request</h1>"
        response_headers = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
        response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
        logging.error("400 Bad Request")

    client_socket.sendall(response)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP_LOCAL, PORTA_LOCAL))
    server_socket.listen(5)
    print(f"Servidor aberto em {IP_LOCAL}:{PORTA_LOCAL}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão de: {client_address}")
        logging.info(f"Conexao de: {client_address}")
        handle_request(client_socket)

if __name__ == "__main__":
    start_server()