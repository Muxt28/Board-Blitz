import socket
import sys
import pickle

class VerifyWin:
    def __init__(self, board, client, gamePlayers):
        self.board = board

        self.clientsConnected = gamePlayers

    def returnBoard(self):
        print('boardSend')
        for elements in self.clientsConnected:
            elements.send(pickle.dumps(self.board))
        
        return self.__VerifyWin()
    
    def __VerifyWin(self):
        print('check')
        win = False

        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                self.clientsConnected[0].send(b'*[ You Have Won ]*')
                self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
                win = True
            elif self.board[rows] == ['O','O','O']:
                self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
                self.clientsConnected[1].send(b'*[ You Have Won ]*')
                win = True

        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if score == ['X','X','X']:
                self.clientsConnected[0].send(b'*[ You Have Won ]*')
                self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
                win = True
            elif score == ['O','O','O']:
                self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
                self.clientsConnected[1].send(b'*[ You Have Won ]*')
                win = True

        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X']:
            self.clientsConnected[0].send(b'*[ You Have Won ]*')
            self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
            win = True
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O','O']:
            self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
            self.clientsConnected[1].send(b'*[ You Have Won ]*')
            win = True
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X','X']:
            self.clientsConnected[0].send(b'*[ You Have Won ]*')
            self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
            win = True
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O','O']:
            self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
            self.clientsConnected[1].send(b'*[ You Have Won ]*')
            win = True
        
        return win

class GameManager:
    def __init__(self, GamePort, portUsed):
        self.portUsed = portUsed

        self.GameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.GameSocket.bind(('0.0.0.0', GamePort))
        self.GameSocket.listen()

        self.clientsConnected = []

        self.running = True
        self.BoxesFilled = 0

        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.board = [['-'for _ in range(3)] for _ in range(3)]

    def Initialise(self):
        while len(self.clientsConnected) != 2:
            ClientCONN, addr = self.GameSocket.accept()
            self.clientsConnected.append(ClientCONN)
        
        return self.GamePlay()
        
    
    def GamePlay(self): 
        win = False
        while (self.running or self.BoxesFilled < 9) and (win == False):
            print(f'Turns : {self.BoxesFilled}')
            if self.BoxesFilled % 2 == 0:
                self.player = self.clientsConnected[0]
                for elements in self.clientsConnected:
                    elements.send(b'\n*[ Player 1 Turn ]*')
                self.currentPlayer = 'X'
            else:
                self.player = self.clientsConnected[1]
                for elements in self.clientsConnected:
                    elements.send(b'\n*[ Player 2 Turn ]*')
                self.currentPlayer = 'O'

            win = VerifyWin.returnBoard(VerifyWin(self.Update_board(), self.player, self.clientsConnected))                                                                                                                                                                            
            print('*[ Sent ]*')
            self.BoxesFilled += 1

        return 'Disconnected'

    def Update_board(self):
        x, y = self.__UserInput()
        self.board[x][y] = self.currentPlayer
        
        return self.board

    def __UserInput(self):
        choice = ''
        while choice not in self.ValidCoordinates:
            self.player.send('>'.encode())
            choice = self.player.recv(1024).decode()

        return int(choice[0]), int(choice[1])

        