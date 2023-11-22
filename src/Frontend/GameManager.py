import ursina
import ursina.mouse as mouse
import ursina.shaders as shaders
import ursina.camera as camera 
import ursina.window as window

import sys
import pickle
from multiprocessing.pool import ThreadPool

sys.path.append("..")
from Backend import Library
from Frontend import Models
import socket

STATES = {
    "IN_MENU" : False,
    "In3x3Single" : False
}

MENU_GLOBAL = False
BOARD_SCENE_GLOBAL = False


class Menu():
    def __init__(self, firstTime=True) -> None:
        STATES["IN_MENU"] = True
        self.onPlayScreen = False
        self.ROOTCAMERAPOS = (8,3.5,3.4)
        self.ROOTCAMERAROT = (0,-130,0)
        self.maxTilt = 10
        self.MainScene = ursina.Entity(model=Models.GetModelPath("Beach"), scale=10, texture = Models.GetTexture("Beach"), shader=shaders.basic_lighting_shader)
        self.Water = ursina.Entity(model=Models.GetModelPath("Water"), scale=10, texture = Models.GetTexture("Water"), shader=shaders.basic_lighting_shader)
        self.XOModel = ursina.Entity(model=Models.GetModelPath("XOModel"), scale=10, shader=shaders.basic_lighting_shader, rotation = (0,100,0), position = (-1,-.5,-.6))
        ursina.invoke(self.showMainUI, delay=(4 if firstTime else 0))
        ursina.camera.position = self.ROOTCAMERAPOS
        ursina.camera.rotation = self.ROOTCAMERAROT
        self.Water.position = self.Water.position + (0,-1.1,0)
        
    def showMainUI(self):
        self.PlayButton = ursina.Button(scale = (.2,.1), text = "Play", position = (-.4,0))
        self.PlayButton.on_click = self.onPlayClick
        self.List = ursina.ButtonList(button_dict= {
            'Single Player' : self.singlePlayerClick,
            'Multiplayer' : self.multiPlayerClick,
            'Go back' : self.goBack
        }, scale = (1,1), position = (-.8,0.1), enabled=False, button_height=1.5)

    def singlePlayerClick(self):
        global MENU_GLOBAL
        global BOARD_SCENE_GLOBAL
        BOARD_SCENE_GLOBAL = ThreeXThreeBoardScene()
        MENU_GLOBAL.destroy()
        pass
    
    def multiPlayerClick(self):
        global MENU_GLOBAL
        global BOARD_SCENE_GLOBAL
        BOARD_SCENE_GLOBAL = MultiplayeBoardScene()
        MENU_GLOBAL.destroy()
        pass

    def goBack(self):
        self.PlayButton.visible = True
        self.List.enabled = False
        pass

    def onPlayClick(self):
        self.PlayButton.visible = False
        self.List.enabled = True
        

    def onUpdate(self):
            x, y, z = mouse.position
            camera.position = self.ROOTCAMERAPOS + (-x*.1,y*.1,0)
            camera.rotation = self.ROOTCAMERAROT + (
                ((((y*150)-window.size.y/2)/window.size.y)*-self.maxTilt),
                ((((-x*150)-window.size.x/2)/window.size.x)*-self.maxTilt),
                0,
            )

    def destroy(self):
        global MENU_GLOBAL
        STATES["IN_MENU"] = False
        ursina.destroy(self.MainScene)
        ursina.destroy(self.Water)
        ursina.destroy(self.XOModel)
        ursina.destroy(self.PlayButton)
        ursina.destroy(self.List)
        MENU_GLOBAL = False


class MultiplayeBoardScene():
    def __init__(self) -> None:
        STATES["In3x3Single"] = True
        self.Board = ursina.Entity(model=Models.GetModelPath("3x3"), collider = "box", shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200), scale=10, onclick = self.onBoardClick)
        self.Back = ursina.Button(scale = (.07, .07/(16/14)), text = "Exit", position = ursina.window.top_left, origin = (-1,1))
        self.Back.on_click = self.destroy
        self.Back.text_entity.scale = 14
        self.hasGameStarted=False
        self.StatusText = ursina.Text(
            text="*[ Connecting To Server ]*",
            position = ursina.window.top,
            origin = (0,1),
            scale = 1.6
            )
        

        self.GameSocket = socket.socket()
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

        self.player = self.GameSocket.recv(1024).decode()
        print(self.player)

        if self.player == '1':
            self.player_Counter = 'X'
            self.opponent_Counter = 'O'
        else:
            self.player_Counter = 'O'
            self.opponent_Counter = 'X'
    


    def onBoardClick(self):
        pass

    def setStatusText(self, text):
        self.StatusText.text = text
    
    def startGame(self):
        if self.hasGameStarted:
            return
        self.hasGameStarted = True
        # self.CurrentTurn = "X"
    
    def getPosFromCoords(self, gameCoord):
        XROW = 0
        YROW = 0
        if gameCoord.X <= -55:
            XROW = 0
        elif gameCoord.X > -55 and gameCoord.X <= 50:
            XROW = 1
        elif gameCoord.X > 50:
            XROW = 2
        if gameCoord.Z <= -55:
            YROW = 2
        elif gameCoord.Z > -55 and gameCoord.Z <= 50:
            YROW = 1
        elif gameCoord.Z > 50:
            YROW = 0
        gameCoords = str(YROW) + str(XROW)
        coordDict = {
            "00" : (-107,7,107),
            "01" : (0,7,107),
            "02" : (107,7,107),
            "10" : (-107,7,0),
            "11" : (0,7,0),
            "12" : (107,7,0),
            "20" : (-107,7,-107),
            "21" : (0,7,-107),
            "22" : (107,7,-107),
        }
        return coordDict[gameCoords]

    def placeX(self, coords):
        newX = ursina.Entity(model=Models.GetModelPath("X"), shader=shaders.basic_lighting_shader, scale=10)
        newX.position = self.getPosFromCoords(coords)    
        
    
    def placeO(self, coords):
        newO = ursina.Entity(model=Models.GetModelPath("O"), shader=shaders.basic_lighting_shader, scale=10)
        newO.position = self.getPosFromCoords(coords)    
        pass

    def handleMouseClick(self, pos, BoxesFilled, data):        
        coordinates = {
            "00" : (-107,7,107),
            "01" : (0,7,107),
            "02" : (107,7,107),
            "10" : (-107,7,0),
            "11" : (0,7,0),
            "12" : (107,7,0),
            "20" : (-107,7,-107),
            "21" : (0,7,-107),
            "22" : (107,7,-107),
        }

        if data != '*[ Your Turn ]*':
            coords = self.GameSocket.recv(1024).decode()
            if self.opponent_Counter == 'X':
                self.placeX(coords)
            else:
                self.placeO(coords)


        else:
            key_list = list(coordinates.keys())
            val_list = list(coordinates.values())

            position = val_list.index(self.getPosFromCoords(pos))

            xy = key_list[position]
            x, y = int(xy[0]), int(xy[1])

            if self.player_Counter == 'X':
                self.placeX(coordinates[coords])
            else:
                self.placeO(coordinates[coords])


    def destroy(self):
        global MENU_GLOBAL
        STATES["In3x3Single"] = False
        ursina.destroy(self.Board)
        ursina.destroy(self.Back)
        try:
            ursina.destroy(self.StatusText)
        except AttributeError:
            pass
        MENU_GLOBAL = Menu(False)

    def onUpdate(self, mouseCoords):
        if mouseCoords!=None:
            pass


class ThreeXThreeBoardScene():
    def __init__(self) -> None:
        STATES["In3x3Single"] = True
        self.Board = ursina.Entity(model=Models.GetModelPath("3x3"), collider = "box", shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200), scale=10, onclick = self.onBoardClick)
        self.Back = ursina.Button(scale = (.07, .07/(16/14)), text = "Exit", position = ursina.window.top_left, origin = (-1,1))
        self.Back.on_click = self.destroy
        self.Back.text_entity.scale = 14
        self.hasGameStarted=False
        # self.StatusText = ursina.Text(
        #     text="The game will be starting soon...",
        #     position = ursina.window.top,
        #     origin = (0,1),
        #     scale = 1.6
        #     )
        
        self.startGame()

    def onBoardClick(self):
        pass

    def setStatusText(self, text):
        self.StatusText.text = text
    
    def startGame(self):
        if self.hasGameStarted:
            return 1
        self.hasGameStarted = True
        # self.CurrentTurn = "X"
    
    def getPosFromCoords(self, gameCoord):
        XROW = 0
        YROW = 0
        if gameCoord.X <= -55:
            XROW = 0
        elif gameCoord.X > -55 and gameCoord.X <= 50:
            XROW = 1
        elif gameCoord.X > 50:
            XROW = 2
        if gameCoord.Z <= -55:
            YROW = 2
        elif gameCoord.Z > -55 and gameCoord.Z <= 50:
            YROW = 1
        elif gameCoord.Z > 50:
            YROW = 0
        gameCoords = str(YROW) + str(XROW)
        coordDict = {
            "00" : (-107,7,107),
            "01" : (0,7,107),
            "02" : (107,7,107),
            "10" : (-107,7,0),
            "11" : (0,7,0),
            "12" : (107,7,0),
            "20" : (-107,7,-107),
            "21" : (0,7,-107),
            "22" : (107,7,-107),
        }
        return coordDict[gameCoords]

    def placeX(self, coords):
        newX = ursina.Entity(model=Models.GetModelPath("X"), shader=shaders.basic_lighting_shader, scale=10)
        newX.position = self.getPosFromCoords(coords)    
        
    
    def placeO(self, coords):
        newO = ursina.Entity(model=Models.GetModelPath("O"), shader=shaders.basic_lighting_shader, scale=10)
        newO.position = self.getPosFromCoords(coords)    
        pass

    def handleMouseClick(self, pos, BoxesFilled, board):        
        thread = ThreadPool(processes=1)
        coordinates = {
            "00" : (-107,7,107),
            "01" : (0,7,107),
            "02" : (107,7,107),
            "10" : (-107,7,0),
            "11" : (0,7,0),
            "12" : (107,7,0),
            "20" : (-107,7,-107),
            "21" : (0,7,-107),
            "22" : (107,7,-107),
        }

        key_list = list(coordinates.keys())
        val_list = list(coordinates.values())

        position = val_list.index(self.getPosFromCoords(pos))

        xy = key_list[position]
        x, y = int(xy[0]), int(xy[1])
        if board[x][y] == '-':
            threadReturn = thread.apply_async(Library.LocalPlayer.GamePlay, (Library.LocalPlayer(BoxesFilled, key_list[position], board),))
            win, board = threadReturn.get()
        else:
            return 'NOT VALID', board

        if pos != None:
            if BoxesFilled % 2 == 0:
                self.placeX(pos)
            else:
                self.placeO(pos)

        if win  == '*[ Player 1 has Won ]*' or win == '*[ Player 2 has Won ]*':
            return win, board
        else:
            return None, board


    def destroy(self):
        global MENU_GLOBAL
        STATES["In3x3Single"] = False
        ursina.destroy(self.Board)
        ursina.destroy(self.Back)
        try:
            ursina.destroy(self.StatusText)
        except AttributeError:
            pass
        MENU_GLOBAL = Menu(False)

    def onUpdate(self, mouseCoords):
        if mouseCoords!=None:
            pass
