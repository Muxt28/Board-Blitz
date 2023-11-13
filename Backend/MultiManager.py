import socket
import sys
import pickle

class VerifyWin:
    def __init__(self, board, client, gamePlayers):
        self.board = board

        self.clientsConnected = gamePlayers

    def returnBoard(self):
        for elements in self.clientsConnected:
            elements.send(pickle.dumps(self.board))
        var = self.__VerifyWin()
        if var == True:
            return True
        else:
            return False
    
    def __VerifyWin(self):
        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                self.clientsConnected[0].send(b'*[ You Have Won ]*')
                self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
                return False
            elif self.board[rows] == ['O','O','O']:
                self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
                self.clientsConnected[1].send(b'*[ You Have Won ]*')
                return False

        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if score == ['X','X','X']:
                self.clientsConnected[0].send(b'*[ You Have Won ]*')
                self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
                return False
            elif score == ['O','O','O']:
                self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
                self.clientsConnected[1].send(b'*[ You Have Won ]*')
                return False

        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X']:
            self.clientsConnected[0].send(b'*[ You Have Won ]*')
            self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
            return False
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O','O']:
            self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
            self.clientsConnected[1].send(b'*[ You Have Won ]*')
            return False
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X','X']:
            self.clientsConnected[0].send(b'*[ You Have Won ]*')
            self.clientsConnected[1].send(b'*[ Player 1 has Won ]*')
            return False
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O','O']:
            self.clientsConnected[0].send(b'*[ Player 2 has Won ]*')
            self.clientsConnected[1].send(b'*[ You Have Won ]*')
            return False
        
        return True


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
        
        if self.GamePlay() == 'Disconnected':
            print('Bye')
            return 'Disconnected'
    
    def GamePlay(self):
        while self.running and self.BoxesFilled < 9:
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

            self.running = VerifyWin.returnBoard(VerifyWin(self.Update_board(), self.player, self.clientsConnected))
            print(self.running)
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
            self.player.send(b'>')
            choice = self.player.recv(2048).decode()

        return int(choice[0]), int(choice[1])

        