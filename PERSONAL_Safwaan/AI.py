# UH DONT TOUCH THIS YET IM WORKING ON IT
from random import randint


class AI:
    def __init__(self):
        self.board = [['-' for columns in range(3)] for rows in range(3)]
        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.startPos = ['00', '02', '11', '20', '22']

        self.player_choose = randint(0,1)

    def __selectStartPos(self):
        return self.startPos[randint(0, 4)]
        
    def startAI(self):
        x,y = self.__selectRandomPos().split(' ')
        self.board[x][y] 
        

    def choosePlayer():
        
        if self.player_choose == 0:
            self.startAI()
        else:
            #Player starts



AI.choosePlayer(AI())
          
