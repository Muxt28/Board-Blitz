import socket
import sys
import pickle


class VerifyWin:
    def __init__(self, board):
        self.board = board

    def returnBoard(self):
        for rows in self.board:
                print(f"{' '.join(rows)}")
        self.__VerifyWin()
    
    def __VerifyWin(self): 
        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                print('*[ Player 1 has Won ]*')
                sys.exit()
            elif self.board[rows] == ['O','O','O']:
                print('*[ Player 2 has Won ]*')
                sys.exit()
        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if score == ['X','X','X']:
                print('*[ Player 1 has Won ]*')
                sys.exit()
            elif score == ['O','O','O']:
                print('*[ Player 2 has Won ]*')
                sys.exit()
        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X']:
            print('*[ Player 1 has Won ]*')
            sys.exit()
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O','O']:
            print('*[ Player 2 has Won ]*')
            sys.exit()
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X','X']:
            print('*[ Player 1 has Won ]*')
            sys.exit()
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O','O']:
            print('*[ Player 2 has Won ]*')
            sys.exit()
    

class LocalPlayer:
    def __init__(self, q):
        self.inputQueue = q
        self.running = True
        self.BoxesFilled = 0

        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.board = [['-'for _ in range(3)] for _ in range(3)]
        self.GamePlay()
    
    def GamePlay(self):
        while self.running and self.BoxesFilled < 9:
            if self.BoxesFilled % 2 == 0:
                print(f'\n*[ Player 1 Turn ]*')
                self.currentPlayer = 'X'
            else:
                print(f'\n*[ Player 2 Turn ]*')
                self.currentPlayer = 'O'

            VerifyWin.returnBoard(VerifyWin(self.Update_board()))
            self.BoxesFilled += 1

    def Update_board(self):
        
        x, y = self.__UserInput()
        self.board[x][y] = self.currentPlayer

        return self.board

    def __UserInput(self):
        choice = ''
        while choice not in self.ValidCoordinates:
            choice = input('Please Enter A Coordinate : ')

        return int(choice[0]), int(choice[1])


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

#Multiplayer.Game_Manager(Multiplayer())