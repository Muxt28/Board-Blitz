import socket
import sys
import pickle

class Multiplayer:
    def __init__(self):
        self.GameSocket = socket.socket()
        
        self.running = True

    def __ContactServer(self):
        try:
            self.GameSocket.connect(('35.176.207.55', 5555))
        except ConnectionRefusedError:
            self.GameSocket.connect(('35.176.207.55', 5556))

        print(self.GameSocket.recv(1024).decode())

        self.GameSocket.send(input('Enter Code : ').encode())
        
        port = int(self.GameSocket.recv(1024).decode())
        print(f'Port : {port}')
        self.GameSocket.close()

        self.GameSocket = socket.socket()
        self.GameSocket.connect(('35.176.207.55', port))

        self.playerNumber = self.GameSocket.recv(1024).decode()

    def Game_Manager(self):
        self.__ContactServer()

        while self.running:
            Msg = self.GameSocket.recv(1024)
            try:
                board = pickle.loads(Msg)
                for rows in board:
                    print(' '.join(rows))
            except Exception:
                Msg = Msg.decode()
                if Msg == '*[ Your Turn ]*' or Msg == '*[ Box Occupied ]*':
                    self.GameSocket.send(input('Enter Coordinates : ').encode())
                    print('*[ Sent ]*')
                else:
                    if Msg != '':
                        print(f'{Msg}')
