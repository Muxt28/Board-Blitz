import socket
import sys
import pickle
import threading
from queue import Queue


class VerifyWin:    
    def Verify(board): 
        for rows in range(3):
            if board[rows] == ['X','X','X']:
                return '*[ Player 1 has Won ]*'
            elif board[rows] == ['O','O','O']:
                return '*[ Player 2 has Won ]*'
        # Check Vertically :
        for columns in range(3):
            score = [board[0][columns], board[1][columns], board[2][columns]]
            if score == ['X','X','X']:
                return '*[ Player 1 has Won ]*'
            elif score == ['O','O','O']:
                return '*[ Player 2 has Won ]*'
        # Check Diagonally :
        if [board[0][0], board[1][1], board[2][2]] == ['X','X','X']:
            return '*[ Player 1 has Won ]*'
        elif [board[0][0], board[1][1], board[2][2]] == ['O','O','O']:
            return '*[ Player 2 has Won ]*'
        elif [board[0][2], board[1][1], board[2][0]] == ['X','X','X']:
            return '*[ Player 1 has Won ]*'
        elif [board[0][2], board[1][1], board[2][0]] == ['O','O','O']:
            return '*[ Player 2 has Won ]*'

        return 'NO WIN'
    

class LocalPlayer:
    def __init__(self, boxesFilled, coords, board):
        self.running = True
        self.BoxesFilled = boxesFilled

        self.x, self.y = int(coords[0]), int(coords[1])
        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.board = board
        self.GamePlay()
    
    def GamePlay(self):
        while self.running and self.BoxesFilled < 9:
            # print(self.BoxesFilled)
            if self.BoxesFilled % 2 == 0:
                self.currentPlayer = 'X'
            else:
                self.currentPlayer = 'O'

            win = VerifyWin.Verify(self.Update_board())
            return win, self.board
            
    def Update_board(self):
        self.board[self.x][self.y] = self.currentPlayer
        return self.board
