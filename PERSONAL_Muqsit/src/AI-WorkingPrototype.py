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
        print(chr(27) + "[2J")
        for rows in self.board:
                print(f"{' '.join(rows)}")
        print('\n')
        return self.__VerifyWin()

    def __VerifyWin(self):

        for rows in range(3):
            if self.board[rows] == ['X','X','X']:
                print(f'*[ {self.x} has Won ]*')
                return False
            elif self.board[rows] == ['O','O','O']:
                print(f'*[ {self.o} has Won ]*')
                return False
        # Check Vertically :
        for columns in range(3):
            score = [self.board[0][columns], self.board[1][columns], self.board[                                                                                        2][columns]]
            if score == ['X','X','X']:
                print(f'*[ {self.x} has Won ]*')
                return False
            elif score == ['O','O','O']:
                print(f'*[ {self.o} has Won ]*')
                return False
        # Check Diagonally :
        if [self.board[0][0], self.board[1][1], self.board[2][2]] == ['X','X','X                                                                                        ']:
            print(f'*[ {self.x} has Won ]*')
            return False
        elif [self.board[0][0], self.board[1][1], self.board[2][2]] == ['O','O',                                                                                        'O']:
            print(f'*[ {self.o} has Won ]*')
            return False
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['X','X',                                                                                        'X']:
            print(f'*[ {self.x} has Won ]*')
            return False
        elif [self.board[0][2], self.board[1][1], self.board[2][0]] == ['O','O',                                                                                        'O']:
            print(f'*[ {self.o} has Won ]*')
            return False

        return True


class AI:
    def __init__(self):
        self.running = True
        self.BoxesFilled = 0

        self.currentPlayer = ''

        self.ValidCoordinates = ['00', '01', '02', '10', '11', '12', '20', '21',                                                                                         '22']
        self.board = [['-'for _ in range(3)] for _ in range(3)]

        self.StartingMove = ['00', '02', '20', '22', '11']

        self.First_Player = randint(0, 1)
        # self.First_Player = 0

        # 0 = AI
        # 1 = Player


    def __displayBoard(self):
        print(chr(27) + "[2J")
        for rows in self.board:
            print(' '.join(rows))
        print('\n')

    def setCounters(self):
        if self.First_Player == 0:
            self.player_Counter, self.Ai_Counter = 'O', 'X'

            x,y = self.StartingMove[randint(0, 4)]
            self.board[int(x)][int(y)] = self.Ai_Counter
            self.__displayBoard()
            self.BoxesFilled += 1

        else:
            self.player_Counter, self.Ai_Counter = 'X', 'O'
            self.__Player_Manager()

        while self.running:
            if self.BoxesFilled % 2 == 0:
                AI_Manager.Options(AI_Manager(self.player_Counter, self.Ai_Counter, self.board, self.ValidCoordinates))
            elif self.BoxesFilled % 2 != 0:
                self.__Player_Manager()

            self.running = VerifyWin.returnBoard(VerifyWin(self.board, self.First_Player))

            self.BoxesFilled += 1

            if self.BoxesFilled == 9:
                print("*[ It's A Draw ]*")
                self.running = False

        return self.board


    def __Player_Manager(self):
        choice = 'string'
        while choice not in self.ValidCoordinates and type(choice) != 'string':
            choice = input(':: > ')
            x, y = int(choice[0]), int(choice[1])
            if self.board[x][y] != '-':
                choice = ''
        self.board[x][y] = self.player_Counter


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



AI.setCounters(AI())
# for rows in board:
#     print(' '.join(rows))