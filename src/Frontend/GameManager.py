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
    "In3x3Single" : False
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
        text = ursina.Text("Multiplayer is currently not supported!", color=ursina.color.red)
        ursina.invoke(ursina.destroy, text, delay=2)
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
    def __init__(self) -> None:
        STATES["In3x3Single"] = True
        self.Board = ursina.Entity(model=Models.GetModelPath("3x3"), shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200), scale=10)
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

    def setStatusText(self, text):
        self.StatusText.text = text
    
    def startGame(self):
        if self.hasGameStarted:
            print("The game instance has already started!")
            return 1;
        self.hasGameStarted = True
        # locked session
        newGameInstance = Thread(target=Library.LocalPlayer, args=(self.inputQueue))
        self.inputQueue = Queue(maxsize=0)
        #newGameInstance.__UserInput = __UserInputFrontend
        newGameInstance.start()
        print("started game thread from GameManager")
    
    def.getPosFromCoords(gameCoord):

        pass

    def placeX(coords):
        newX = ursina.Entity(Models.GetModelPath("X"), shader=shaders.basic_lighting_shader, scale=10)
        newX.Position = self.getPosFromCoords(coords)
        # position newX with coords
        # handle 3d stuff here... and THEN 

        # do ur backend ting here
    
    def placeO():
        # handle 3d stuff here.. and then

        # backend


    def destroy(self):
        global MENU_GLOBAL
        STATES["In3x3Single"] = False
        ursina.destroy(self.Board)
        ursina.destroy(self.Back)
        ursina.destroy(self.StatusText)

        MENU_GLOBAL = Menu(False)

    def onUpdate(self):
        
        pass