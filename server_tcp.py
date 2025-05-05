from socket import *
from random import randint
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

serverPort = 12001
serverName = 'localhost'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)

num = randint(0, 100)
logging.info(f"Servidor iniciado e pronto para conexões na porta {serverPort}")
logging.debug(f"Número secreto (DEBUG): {num}")

while True:
    connectionSocket, addr = serverSocket.accept()
    logging.info(f"Conexão estabelecida com {addr}")
    
    while True:
        data = connectionSocket.recv(1024).decode('utf-8')
        if not data:
            logging.info("Conexão encerrada pelo cliente")
            break
            
        try:
            guess = int(data)
            logging.info(f"Recebido palpite: {guess}")
            
            if guess < num:
                response = f'O número {guess} é menor que o número secreto'
                logging.debug(response)
            elif guess > num:
                response = f'O número {guess} é maior que o número secreto'
                logging.debug(response)
            else:
                response = f'Parabéns! Você acertou o número {num}'
                logging.info(f"Cliente acertou o número: {num}")
                connectionSocket.send(response.encode('utf-8'))
                break
                
            connectionSocket.send(response.encode('utf-8'))
        except ValueError:
            error_msg = f"Valor inválido recebido: {data}"
            logging.warning(error_msg)
            connectionSocket.send('Por favor, digite um número válido'.encode('utf-8'))
    
    connectionSocket.close()