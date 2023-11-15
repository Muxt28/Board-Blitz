import ursina
import ursina.mouse as mouse
import ursina.shaders as shaders
import ursina.camera as camera 
import ursina.window as window

STATES = {
    "IN_MENU" : False
}

from Frontend import Models

class Menu():
    def __init__(self) -> None:
        STATES["IN_MENU"] = True
        self.onPlayScreen = False
        self.ROOTCAMERAPOS = (8,3.5,3.4)
        self.ROOTCAMERAROT = (0,-130,0)
        self.maxTilt = 10
        self.MainScene = ursina.Entity(model=Models.GetModelPath("Beach"), scale=10, texture = Models.GetTexture("Beach"), shader=shaders.basic_lighting_shader)
        self.Water = ursina.Entity(model=Models.GetModelPath("Water"), scale=10, texture = Models.GetTexture("Water"), shader=shaders.basic_lighting_shader)
        #self.Trees = ursina.Entity(model=Models.GetModelPath("Trees"), scale=10)
        self.XOModel = ursina.Entity(model=Models.GetModelPath("XOModel"), scale=10, shader=shaders.basic_lighting_shader, rotation = (0,100,0), position = (-1,-.5,-.6))
        ursina.invoke(self.showMainUI, delay=4)
        ursina.camera.position = self.ROOTCAMERAPOS
        ursina.camera.rotation = self.ROOTCAMERAROT
        self.Water.position = self.Water.position + (0,-1.1,0)
        
    def showMainUI(self):
        self.PlayButton = ursina.Button(scale = (.2,.1), text = "Play", position = (-.4,0))
        self.PlayButton.on_click = self.onPlayClick
        self.List = ursina.ButtonList(button_dict= {
            'SinglePlayer' : self.singlePlayerClick,
            'MultiPlayer' : self.multiPlayerClick,
            'Go back' : self.goBack
        }, scale = (1,1), position = (-.8,0.1), visible=False)

    def singlePlayerClick(self):
        pass

    def multiPlayerClick(self):
        pass

    def goBack(self):
        self.PlayButton.visible = True
        self.List.visible = False
        pass

    def onPlayClick(self):
        print("click moment")
        self.PlayButton.visible = False
        self.List.visible = True
        

    def onUpdate(self):
            x, y, z = mouse.position
            #print(ROOTCAMERAPOS)
            camera.position = self.ROOTCAMERAPOS + (-x*.1,y*.1,0)
            camera.rotation = self.ROOTCAMERAROT + (
                ((((y*150)-window.size.y/2)/window.size.y)*-self.maxTilt),
                ((((-x*150)-window.size.x/2)/window.size.x)*-self.maxTilt),
                0,
            )

    def __del__(self):
        #Cleanup
        ursina.destroy(self.MainScene)
        ursina.destroy(self.Water)
        ursina.destroy(self.XOModel)
        ursina.destroy(self.PlayButton)
        ursina.destroy(self.List)
        #ursina.destroy(self.Trees)
        STATES["IN_MENU"] = False


class ThreeXThreeBoardScene():
    def __init__(self) -> None:
        pass

    def __del__(self):
        pass

    def onUpdate(self):
        pass