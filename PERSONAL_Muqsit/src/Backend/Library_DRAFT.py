
class VerifyWin:
    def __init__(self, board):
        return

class LocalPlayer:
    def __init__(self):
        # self.inputQueue = inputQueue 
        self.running = True
        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.board = [['-'for _ in range(3)] for _ in range(3)]

    def GamePlay(self):
        if self.BoxesFilled % 2 == 0:
            print(f'\n*[ Player 1 Turn ]*')
            self.currentPlayer = 'X'
        else:
            print(f'\n*[ Player 2 Turn ]*')
            self.currentPlayer = 'O'

        Move = self.User_Input()
        if Move != False:
            VerifyWin(Move)
            self.BoxesFilled += 1
            return 
        else:
            print('hi')
            return 'MOVE NOT VALID'
            
    def User_Input(self):
        choice = ''
        while choice not in self.ValidCoordinates:
            choice = input('Choice : ')
            if choice not in self.ValidCoordinates:
                return False

        self.ValidCoordinates.remove(choice)
        self.Update_board(int(choice[0]), int(choice[1]))
    
    def Update_board(self, x, y):
        self.board[x][y] = self.currentPlayer
        return self.board
    

# Move = 'MOVE NOT VALID'
# while Move == 'MOVE NOT VALID':
#     Move = LocalPlayer.GamePlay(LocalPlayer())
#     print(Move)
