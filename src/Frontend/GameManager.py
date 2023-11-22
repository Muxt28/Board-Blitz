import ursina
import ursina.mouse as mouse
import ursina.shaders as shaders
import ursina.camera as camera 
import ursina.window as window

import sys
from queue import Queue
from threading import Thread

sys.path.append("..")
from Backend import Library
from Frontend import Models


STATES = {
    "IN_MENU" : False,
    "In3x3Single" : False,
    "In3x3Multiplayer" : False
}

MENU_GLOBAL = False
BOARD_SCENE_GLOBAL = False

#from Main import Menu as MENUGLOBAL

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
        #ThreeXThreeBoardScene()
        #self.__del__()
        global MENU_GLOBAL
        global BOARD_SCENE_GLOBAL
        BOARD_SCENE_GLOBAL = ThreeXThreeBoardScene()
        MENU_GLOBAL.destroy()
        pass
    
    def multiPlayerClick(self):
        #text = ursina.Text("Multiplayer is currently not supported!", color=ursina.color.red)
        #ursina.invoke(ursina.destroy, text, delay=2)
        global MENU_GLOBAL
        global BOARD_SCENE_GLOBAL
        BOARD_SCENE_GLOBAL = MultiPlayer3x3Scene()
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
            #print(ROOTCAMERAPOS)
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
        #ursina.destroy(self.Trees)
class ThreeXThreeBoardScene():
    def __init__(self, gameType="In3x3Single") -> None:
        self.currentGameType = gameType
        STATES[self.currentGameType] = True
        self.Board = ursina.Entity(model=Models.GetModelPath("3x3"), collider = "box", shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200), scale=10, onclick = self.onBoardClick)
        self.Back = ursina.Button(scale = (.07, .07/(16/14)), text = "Exit", position = ursina.window.top_left, origin = (-1,1))
        self.Back.on_click = self.destroy
        self.Back.text_entity.scale = 14
        self.hasGameStarted=False
        self.StatusText = ursina.Text(
            text="The game will be starting soon...",
            position = ursina.window.top,
            origin = (0,1),
            scale = 1.6
            )
        self.startGame()
        #self.Text = ursina.Text("The game is starting soon...")
    def onBoardClick(self):
        print("clicked board..")

    def setStatusText(self, text):
        self.StatusText.text = text
    
    def startGame(self):
        if self.hasGameStarted:
            print("The game instance has already started!")
            return 1;
        self.hasGameStarted = True
        # locked session
        self.inputQueue = Queue(maxsize=0)
        newGameInstance = Thread(target=Library.LocalPlayer, args=(self.inputQueue))
        
        #newGameInstance.__UserInput = __UserInputFrontend
        newGameInstance.start()
        print("started game thread from GameManager")
        self.CurrentTurn = "X"
    
    def getPosFromCoords(self, gameCoord):
        # gives in mouse coords, returns board coords
        print(gameCoord)
        XROW = 0;
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
        newX = ursina.Entity(model=Models.GetModelPath("X"), shader=shaders.basic_lighting_shader, scale=10, color=ursina.color.red)
        newX.position = self.getPosFromCoords(coords)    
        # position newX with coords
        # handle 3d stuff here... and THEN 

        # do ur backend ting here
    
    def placeO(self, coords):
        # handle 3d stuff here.. and then
        newO = ursina.Entity(model=Models.GetModelPath("O"), shader=shaders.basic_lighting_shader, scale=10, color=ursina.color.cyan)
        newO.position = self.getPosFromCoords(coords)    
        pass
        # backend

    def handleMouseClick(self, pos):
        print("left mouse  button clicked!")
        if pos != None:
            if self.CurrentTurn == "X":
                self.placeX(pos)
                # place X
                self.CurrentTurn = "O"
            else:
                # place O
                self.placeO(pos)
                self.CurrentTurn = "X"


    def destroy(self):
        global MENU_GLOBAL
        STATES[self.currentGameType] = False
        ursina.destroy(self.Board)
        ursina.destroy(self.Back)
        ursina.destroy(self.StatusText)
        MENU_GLOBAL = Menu(False)

    def onUpdate(self, mouseCoords):
        if mouseCoords!=None:
            print(mouseCoords)
        pass


class MultiPlayer3x3Scene:
    def __init__(self, gameType="In3x3Multiplayer") -> None:
        self.currentGameType = gameType
        self.gradient = ursina.Entity(model='quad', texture='vertical_gradient', parent=camera.ui, scale=(camera.aspect_ratio,1), color=ursina.color.hsv(240,.6,.1,.75))
        self.code_field = ursina.InputField(y=-.12, limit_content_to='0123456789', default_value='1024', active=True)
        self.code_field.text = ''
        self.join_button = ursina.Button(text='Join', scale=.1, color=ursina.color.cyan.tint(-.4), y=-.26, on_click=self.onCodeEntered).fit_to_text()

    def onCodeEntered(self):
        self.userInputtedCode = self.code_field.text
        ursina.destroy(self.gradient)
        ursina.destroy(self.code_field)
        ursina.destroy(self.join_button)
        print(f"user inputted code was {self.userInputtedCode}")
        STATES[self.currentGameType] = True
        self.Board = ursina.Entity(model=Models.GetModelPath("3x3"), collider = "box", shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200), scale=10, onclick = self.onBoardClick)
        self.Back = ursina.Button(scale = (.07, .07/(16/14)), text = "Exit", position = ursina.window.top_left, origin = (-1,1))
        self.Back.on_click = self.destroy
        self.Back.text_entity.scale = 14
        self.hasGameStarted=False
        self.StatusText = ursina.Text(
            text="The game will be starting soon...",
            position = ursina.window.top,
            origin = (0,1),
            scale = 1.6
            )
        self.startGame()

        #self.Text = ursina.Text("The game is starting soon...")
    def onBoardClick(self):
        print("clicked board..")

    def setStatusText(self, text):
        self.StatusText.text = text
    
    def startGame(self):
        if self.hasGameStarted:
            print("The game instance has already started!")
            return 1;
        self.hasGameStarted = True
        # locked session
        self.inputQueue = Queue(maxsize=0)
        newGameInstance = Thread(target=Library.LocalPlayer, args=(self.inputQueue))
        
        #newGameInstance.__UserInput = __UserInputFrontend
        newGameInstance.start()
        print("started game thread from GameManager")
        self.CurrentTurn = "X"
    
    def getPosFromCoords(self, gameCoord):
        # gives in mouse coords, returns board coords
        print(gameCoord)
        XROW = 0;
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
        # position newX with coords
        # handle 3d stuff here... and THEN 

        # do ur backend ting here
    
    def placeO(self, coords):
        # handle 3d stuff here.. and then
        newO = ursina.Entity(model=Models.GetModelPath("O"), shader=shaders.basic_lighting_shader, scale=10)
        newO.position = self.getPosFromCoords(coords)    
        pass
        # backend

    def handleMouseClick(self, pos):
        print("left mouse  button clicked!")
        if pos != None:
            if self.CurrentTurn == "X":
                self.placeX(pos)
                # place X
                self.CurrentTurn = "O"
            else:
                # place O
                self.placeO(pos)
                self.CurrentTurn = "X"


    def destroy(self):
        global MENU_GLOBAL
        STATES[self.currentGameType] = False
        ursina.destroy(self.Board)
        ursina.destroy(self.Back)
        ursina.destroy(self.StatusText)
        MENU_GLOBAL = Menu(False)

    def onUpdate(self, mouseCoords):
        if mouseCoords!=None:
            print(mouseCoords)
        pass