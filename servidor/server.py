import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# IP e porta do servidor
IP_LOCAL = '0.0.0.0'
PORTA_LOCAL = 8000

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("servidor.log"), logging.StreamHandler()]
)

# IP e porta do cliente
ipCliente = None
portaCliente = None

# Função para lidar com os requests
def handle_request(client_socket):

    global status1
    global status2

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
                status1 = False
                status2 = False

                if status1:
                    text1 = 'ON'
                else:
                    text1 = 'OFF'

                if status2:
                    text2 = 'ON'
                else:
                    text2 = 'OFF'

                response_body = f'''
                  <!DOCTYPE html><html>
                    <head>
                      <title>ESP32 Web Server Demo</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1">
                      <style>
                        html {{ font-family: sans-serif; text-align: center; }}
                        body {{ display: inline-flex; flex-direction: column; }}
                        h1 {{ margin-bottom: 1.2em; }}
                        h2 {{ margin: 0; }}
                        div {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; grid-auto-flow: column; grid-gap: 1em; }}
                        .btn {{ background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                               font-size: 2em; text-decoration: none }}
                        .btn.OFF {{ background-color: #333; }}
                      </style>
                    </head
                    <body>
                      <h1>ESP32 Web Server</h1
                      <div>
                        <h2>LED 1</h2>
                        <a href="/toggle/1" class="btn {text1}">{text1}</a>
                        <h2>LED 2</h2>
                        <a href="/toggle/2" class="btn {text2}">{text2}</a>
                      </div>
                    </body>
                  </html>
                '''
                response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
                for i in range(len(request_lines)):
                    logging.info(f"Received request:\n{request_lines[i]}")

            elif method == 'GET' and path == '/toggle/1':
                status1 = not status1

                if status1:
                    text1 = 'ON'
                else:
                    text1 = 'OFF'

                if status2:
                    text2 = 'ON'
                else:
                    text2 = 'OFF'

                response_body = f'''
                  <!DOCTYPE html><html>
                    <head>
                      <title>ESP32 Web Server Demo</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1">
                      <style>
                        html {{ font-family: sans-serif; text-align: center; }}
                        body {{ display: inline-flex; flex-direction: column; }}
                        h1 {{ margin-bottom: 1.2em; }}
                        h2 {{ margin: 0; }}
                        div {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; grid-auto-flow: column; grid-gap: 1em; }}
                        .btn {{ background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                               font-size: 2em; text-decoration: none }}
                        .btn.OFF {{ background-color: #333; }}
                      </style>
                    </head
                    <body>
                      <h1>ESP32 Web Server</h1
                      <div>
                        <h2>LED 1</h2>
                        <a href="/toggle/1" class="btn {text1}">{text1}</a>
                        <h2>LED 2</h2>
                        <a href="/toggle/2" class="btn {text2}">{text2}</a>
                      </div>
                    </body>
                  </html>
                '''
                response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
                response = (response_headers + f"Content-Length: {len(response_body.encode('utf-8'))}\r\n\r\n" + response_body).encode('utf-8')
                for i in range(len(request_lines)):
                    logging.info(f"Received request:\n{request_lines[i]}")

            elif method == 'GET' and path == '/toggle/2':
                status2 = not status2

                if status1:
                    text1 = 'ON'
                else:
                    text1 = 'OFF'

                if status2:
                    text2 = 'ON'
                else:
                    text2 = 'OFF'

                response_body = f'''
                  <!DOCTYPE html><html>
                    <head>
                      <title>ESP32 Web Server Demo</title>
                      <meta name="viewport" content="width=device-width, initial-scale=1">
                      <style>
                        html {{ font-family: sans-serif; text-align: center; }}
                        body {{ display: inline-flex; flex-direction: column; }}
                        h1 {{ margin-bottom: 1.2em; }}
                        h2 {{ margin: 0; }}
                        div {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; grid-auto-flow: column; grid-gap: 1em; }}
                        .btn {{ background-color: #5B5; border: none; color: #fff; padding: 0.5em 1em;
                               font-size: 2em; text-decoration: none }}
                        .btn.OFF {{ background-color: #333; }}
                      </style>
                    </head
                    <body>
                      <h1>ESP32 Web Server</h1
                      <div>
                        <h2>LED 1</h2>
                        <a href="/toggle/1" class="btn {text1}">{text1}</a>
                        <h2>LED 2</h2>
                        <a href="/toggle/2" class="btn {text2}">{text2}</a>
                      </div>
                    </body>
                  </html>
                '''
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