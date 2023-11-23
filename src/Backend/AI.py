from random import randint
from time import sleep


class VerifyWin:
    def __init__(self, board, xo):
        self.board = board

        if xo == 0:
            self.x = 'AI'
            self.o = 'Player'
        else:
            self.o = 'AI'
            self.x = 'Player'

    def returnBoard(self):
        for rows in self.board:
                print(f"{' '.join(rows)}")
        print('\n')
        return self.__VerifyWin()

    def __VerifyWin(self):

        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                return f'*[ {self.x} has Won ]*'
            elif self.board[rows] == ['O','O','O']:
                return '*[ {self.o} has Won ]*'
        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[2][columns]]
            if score == ['X','X','X']:
                return f'*[ {self.x} has Won ]*'
            elif score == ['O','O','O']:
                return f'*[ {self.o} has Won ]*'
        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X']:
            return f'*[ {self.x} has Won ]*'
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O','O']:
            return f'*[ {self.o} has Won ]*'
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X','X']:
            return f'*[ {self.x} has Won ]*'
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O','O']:
            return f'*[ {self.o} has Won ]*'

        return 'NO WIN'


class AI:
    def __init__(self, BoxesFileed, board, First_Player):
        self.running = True
        self.BoxesFilled = BoxesFileed

        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']
        self.board = board

        self.StartingMove = ['00', '02', '20', '22', '11']

        self.First_Player = First_Player

        print('ggggggggggggg')
        # self.First_Player = 0

        # 0 = AI
        # 1 = Player


    def setCounters(self, BoxesFileed, board, First_Player, pos):

        StartingMove = ['00', '02', '20', '22', '11']
        ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']

        if BoxesFileed == 0:
            if First_Player == 0:
                player_Counter, Ai_Counter = 'O', 'X'

                xy = StartingMove[randint(0, 4)]
                print('AI Starts', xy)
                x, y = int(xy[0]), int(xy[1])
                board[int(x)][int(y)] = Ai_Counter

            else:
                player_Counter, Ai_Counter = 'X', 'O'
                board = self.Player_Manager(ValidCoordinates, board, player_Counter, pos, First_Player)
            
            self.running = VerifyWin.returnBoard(VerifyWin(board, First_Player))
        else:

            if First_Player == 0:
                player_Counter, Ai_Counter = 'O', 'X'
            else:
                player_Counter, Ai_Counter = 'X', 'O'

            if self.BoxesFilled % 2 == 0:
                print('AI TURN')
                AI_Manager.Options(AI_Manager(player_Counter, Ai_Counter, board, ValidCoordinates))
            elif self.BoxesFilled % 2 != 0:
                self.Player_Manager(ValidCoordinates, board, player_Counter, pos, First_Player)

            self.running = VerifyWin.returnBoard(VerifyWin(board, First_Player))



        return pos, self.running, board


    def Player_Manager(self, ValidCoordinates, board, player_Counter, pos, First_Player):
        print('Player Turn')
        x, y = int(pos[0]), int(pos[1])
        board[x][y] = player_Counter
        return board
        


class AI_Manager:

    def __init__(self, player_Counter, Ai_Counter, board, Valid_Coordinates):

        self.player_Counter = player_Counter
        self.Ai_Counter = Ai_Counter
        self.board = board

        self.Valid_Coordinates = Valid_Coordinates
        self.StartingMove = ['00', '02', '20', '22', '11']
        sleep(randint(0, 2))

    def Options(self):
        AttackReturn = self.__Attack()
        if AttackReturn == 'DEFENCE' :
            # print(f'Attacking : {AttackReturn}')
            DefenceReturn = self.__Defence()
            if DefenceReturn == 'PLAY':
                # print(f'Defence : {DefenceReturn}')
                playing = self.__play()
                return playing

    def __Defence(self):
    # check Horizantolly :
        for rows in range(3):
            if [self.board[rows][0], self.board[rows][1]] == [self.player_Counter, self.player_Counter]:
                if self.board[rows][2] == '-':
                    self.board[rows][2] = self.Ai_Counter
                    return self.board
            if [self.board[rows][1], self.board[rows][2]] == [self.player_Counter, self.player_Counter]:
                if self.board[rows][0] == '-':
                    self.board[rows][0] = self.Ai_Counter
                    return self.board
            if [self.board[rows][0], self.board[rows][2]] == [self.player_Counter, self.player_Counter]:
                if self.board[rows][1] == '-':
                    self.board[rows][1] = self.Ai_Counter
                    return self.board

        # Check Vertically :
        for columns in range(3):
            if [self.board[0][columns], self.board[1][columns]] == [self.player_Counter, self.player_Counter]:
                if self.board[2][columns] == '-':
                    self.board[2][columns] = self.Ai_Counter
                    return self.board
            if [self.board[1][columns], self.board[2][columns]] == [self.player_Counter, self.player_Counter]:
                if self.board[0][columns] == '-':
                    self.board[0][columns] = self.Ai_Counter
                    return self.board
            if [self.board[0][columns], self.board[2][columns]] == [self.player_Counter, self.player_Counter]:
                if self.board[1][columns] == '-':
                    self.board[1][columns] = self.Ai_Counter
                    return self.board

        # Check Top Left -> Bottom Right :
        if [self.board[0][0], self.board[1][1]] == [self.player_Counter, self.player_Counter]:
            if self.board[2][2] == '-':
                self.board[2][2] = self.Ai_Counter
                return self.board
        if [self.board[1][1], self.board[2][2]] == [self.player_Counter, self.player_Counter]:
            if self.board[0][0] == '-':
                self.board[0][0] = self.Ai_Counter
                return self.board
        if [self.board[0][0], self.board[2][2]] == [self.player_Counter, self.player_Counter]:
            if self.board[1][1] == '-':
                self.board[1][1] = self.Ai_Counter
                return self.board
        # Check Top Right -> Bottom Left :
        if [self.board[0][2], self.board[1][1]] == [self.player_Counter, self.player_Counter]:
            if self.board[2][0] == '-':
                self.board[2][0] = self.Ai_Counter
                return self.board
        if [self.board[1][1], self.board[2][0]] == [self.player_Counter, self.player_Counter]:
            if self.board[0][2] == '-':
                self.board[0][2] = self.Ai_Counter
                return self.board
        if [self.board[0][2], self.board[2][0]] == [self.player_Counter, self.player_Counter]:
            if self.board[1][1] == '-':
                self.board[1][1] = self.Ai_Counter
                return self.board

        return 'PLAY'

    def __Attack(self):
            # check Horizantolly :
        for rows in range(3):
            if [self.board[rows][0], self.board[rows][1]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[rows][2] == '-':
                    self.board[rows][2] = self.Ai_Counter
                    return self.board
            if [self.board[rows][1], self.board[rows][2]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[rows][0] == '-':
                    self.board[rows][0] = self.Ai_Counter
                    return self.board
            if [self.board[rows][0], self.board[rows][2]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[rows][1] == '-':
                    self.board[rows][1] = self.Ai_Counter
                    return self.board

        # Check Vertically :
        for columns in range(3):
            if [self.board[0][columns], self.board[1][columns]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[2][columns] == '-':
                    self.board[2][columns] = self.Ai_Counter
                    return self.board
            if [self.board[1][columns], self.board[2][columns]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[0][columns] == '-':
                    self.board[0][columns] = self.Ai_Counter
                    return self.board
            if [self.board[0][columns], self.board[2][columns]] == [self.Ai_Counter, self.Ai_Counter]:
                if self.board[1][columns] == '-':
                    self.board[1][columns] = self.Ai_Counter
                    return self.board

        # Check Top Left -> Bottom Right :
        if [self.board[0][0], self.board[1][1]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[2][2] == '-':
                self.board[2][2] = self.Ai_Counter
                return self.board
        if [self.board[1][1], self.board[2][2]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[0][0] == '-':
                self.board[0][0] = self.Ai_Counter
                return self.board
        if [self.board[0][0], self.board[2][2]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[1][1] == '-':
                self.board[1][1] = self.Ai_Counter
                return self.board
        # Check Top Right -> Bottom Left :
        if [self.board[0][2], self.board[1][1]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[2][0] == '-':
                self.board[2][0] = self.Ai_Counter
                return self.board
        if [self.board[1][1], self.board[2][0]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[0][2] == '-':
                self.board[0][2] = self.Ai_Counter
                return self.board
        if [self.board[0][2], self.board[2][0]] == [self.Ai_Counter, self.Ai_Counter]:
            if self.board[1][1] == '-':
                self.board[1][1] = self.Ai_Counter
                return self.board

        return 'DEFENCE'


    def __play(self):
        choose = True
        while choose and (len(self.StartingMove) != 0):
            # print('--------')
            randomChoose = self.StartingMove[randint(0, len(self.StartingMove)-1)]
            x, y = int(randomChoose[0]), int(randomChoose[1])
            if self.board[x][y] == '-':
                self.board[x][y] = self.Ai_Counter
                return self.board
            else:
                self.StartingMove.remove(randomChoose)
            if len(self.StartingMove) > 1 :
                coord = self.StartingMove[0]
                x, y = int(coord[0]), int(coord[1])
                if self.board[x][y] == '-':
                    self.board[x][y] = self.Ai_Counter
                    return self.board
                else:
                    self.StartingMove.remove(coord)

        randomChoose = self.Valid_Coordinates[randint(0, len(self.StartingMove)-1)]
        x, y = int(randomChoose[0]), int(randomChoose[1])
        if self.board[x][y] == '-':
            self.board[x][y] = self.Ai_Counter
            return self.board
        else:
            self.Valid_Coordinates.remove(randomChoose)
        if len(self.Valid_Coordinates) > 1 :
            coord = self.Valid_Coordinates[0]
            x, y = coord[0], coord[1]
            if self.board[x][y] == '-':
                self.board[x][y] = self.Ai_Counter
                return self.board
            else:
                self.Valid_Coordinates.remove(coord)




# for rows in board:
#     print(' '.join(rows))
