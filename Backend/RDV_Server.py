import socket
import threading
from random import randint
from MultiManager import GameManager

verificationCode = []
ClientsConnected = []
portsUsed = [5555]

running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

def Check4Opponent(clientCONN):
    LobbyCode = clientCONN.recv(2048).decode()
    if LobbyCode in verificationCode:
        SendPorts(clientCONN, LobbyCode)
    else:
        verificationCode.append(LobbyCode)
        ClientsConnected.append(clientCONN)
    
def SendPorts(clientCONN, LobbyCode):
    player1 = ClientsConnected[verificationCode.index(LobbyCode)]
    player2 = clientCONN

    ClientsConnected.remove(player1)
    verificationCode.remove(LobbyCode)

    # print(f'Player 1 : {player1}\nPlayer 2 : {player2}')

    sent = False
    while sent != True:
        GamePort = randint(1111,4444)
        if GamePort not in portsUsed:
            player1.send(str(GamePort).encode())
            player2.send(str(GamePort).encode())

            portsUsed.append(GamePort)
            sent = True
    
    disconnect = GameManager.Initialise(GameManager(GamePort, portsUsed))
    if disconnect == 'Disconnected':
        portsUsed.remove(GamePort)
    

while running:
    try:
        clientCONN, _ = server.accept()
        clientCONN.send(b'*[ Waiting For Opponent ]*')
        Check4Opponent_Thread = threading.Thread(target = Check4Opponent, args = (clientCONN,))
        Check4Opponent_Thread.start()
    except Exception as e:
        print('*[ Server Error ]*')
