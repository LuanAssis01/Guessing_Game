from socket import *            
from random import randint      
import logging                  
import threading               

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
serverSocket.listen(5)  

logging.info(f"Servidor iniciado e pronto para conexões na porta {serverPort}")

def handle_client(connectionSocket, addr):
    num = randint(0, 100)  
    logging.info(f"Conexão iniciada com {addr} | Número secreto: {num}")

    while True:
        try:
            data = connectionSocket.recv(1024).decode('utf-8')
            if not data:
                logging.info(f"Conexão encerrada por {addr}")
                break

            guess_str, attempts_str = data.split(',')
            guess = int(guess_str)
            attempts = int(attempts_str)

            logging.info(f"[{addr}] Palpite: {guess} (tentativa {attempts})")

            if guess < 0 or guess > 100:
                response = f'O número {guess} está fora do intervalo estabelecido'
            elif guess < num:
                response = f'O número {guess} é menor que o número secreto'
            elif guess > num:
                response = f'O número {guess} é maior que o número secreto'
            else:
                response = f'Parabéns! Você acertou o número {num} após {attempts} tentativas'
                connectionSocket.send(response.encode('utf-8'))
                break

            connectionSocket.send(response.encode('utf-8'))

        except ValueError:
            logging.warning(f"[{addr}] Valor inválido recebido: {data}")
            connectionSocket.send('Por favor, digite um número válido'.encode('utf-8'))

    connectionSocket.close()
    logging.info(f"Conexão finalizada com {addr}")


while True:
    connectionSocket, addr = serverSocket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    client_thread.start()
