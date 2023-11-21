import socket
import sys
import pickle
import threading
from queue import Queue


class VerifyWin:
    def __init__(self, board):
        self.board = board

    def returnBoard(self):
        for rows in self.board:
                print(f"{' '.join(rows)}")
        self.__VerifyWin()
    
    def __VerifyWin(self): 

        win = False

        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                print('*[ Player 1 has Won ]*')
                win = 1
            elif self.board[rows] == ['O','O','O']:
                print('*[ Player 2 has Won ]*')
                win = 2
        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if score == ['X','X','X']:
                print('*[ Player 1 has Won ]*')
                win = 1
            elif score == ['O','O','O']:
                print('*[ Player 2 has Won ]*')
                win = 2
        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X']:
            print('*[ Player 1 has Won ]*')
            win = 1
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O','O']:
            print('*[ Player 2 has Won ]*')
            win = 2
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X','X']:
            print('*[ Player 1 has Won ]*')
            win = 1
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O','O']:
            print('*[ Player 2 has Won ]*')
            win = 2
    
        return win, self.board

class LocalPlayer:
    def __init__(self):
        # self.inputQueue = inputQueue 
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

            Valid = self.Update_board()
            if Valid != False:
                VerifyWin.returnBoard(VerifyWin(Valid))
                self.BoxesFilled += 1
            else:
                return 'MOVE NOT VALID'

    def Update_board(self):
        try:
            x, y = self.__UserInput()
        except Exception:
            return False
        self.board[x][y] = self.currentPlayer

        return self.board

    def __UserInput(self):
        choice = ''
        while choice not in self.ValidCoordinates:
            choice = input('Choice : ')
            if choice not in self.ValidCoordinates:
                # self.backend_Queue = Queue.put('NOT VALID')
                return False
        
        # self.backend_Queue = Queue.put('VALID')
        return int(choice[0]), int(choice[1])
