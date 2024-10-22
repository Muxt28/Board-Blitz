import socket
import threading
from random import randint
from MultiManager import GameManager

verificationCode = []
ClientsConnected = []
portsUsed = [5555, 5556]

running = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(('0.0.0.0', 5555))
except Exception:
    server.bind(('0.0.0.0', 5556))
    
server.listen()

def Check4Opponent(clientCONN):
    LobbyCode = clientCONN.recv(1024).decode()
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
    if GameManager.Initialise(GameManager(GamePort)) == 'Disconnected':
        portsUsed.remove(GamePort)
    

while running: 
    try:
        clientCONN, _ = server.accept()
        clientCONN.send(b'*[ Waiting For Opponent ]*')
        Check4Opponent_Thread = threading.Thread(target = Check4Opponent, args = (clientCONN,))
        Check4Opponent_Thread.start()
    except Exception as e:
        print('*[ Server Error ]*')
