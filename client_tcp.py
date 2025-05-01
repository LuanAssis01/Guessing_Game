from socket import *

serverName = 'localhost'
serverPort = 12001

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print('Jogo de Adivinhação\nTente adivinhar o número entre 0 e 100')

while True:
    guess = input("Digite um número (ou 'sair' para terminar): ")
    if guess.lower() == 'sair':
        break
        
    clientSocket.send(guess.encode('utf-8'))
    response = clientSocket.recv(1024).decode('utf-8')
    print("Resposta do servidor:", response)
    
    if 'Parabéns' in response:
        break

clientSocket.close()