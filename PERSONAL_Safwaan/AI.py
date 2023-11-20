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
    #These moves will only be called when the player starts first and takes the middle - its that V shape
    def move10(self):
        self.board[1][0] = "O"
    def move21(self):
        self.board[2][1] = "O"
    def move12(self):
        self.board[1][2] = "O"

    def choosePlayer(self):
        if self.player_choose == 0:
            self.startAI()
        else:
            #player starts

    def playerStart(self):
        if #p
    def aiStart(self):


        
            



AI.choosePlayer(AI())
