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
        self.ROOTCAMERAPOS = (8,3.5,3.4)
        self.ROOTCAMERAROT = (0,-130,0)
        self.maxTilt = 10
        self.MainScene = ursina.Entity(model=Models.GetModelPath("Beach"), scale=10, texture = Models.GetTexture("Beach"), shader=shaders.basic_lighting_shader)
        self.Water = ursina.Entity(model=Models.GetModelPath("Water"), scale=10, texture = Models.GetTexture("Water"), shader=shaders.basic_lighting_shader)
        #self.Trees = ursina.Entity(model=Models.GetModelPath("Trees"), scale=10)
        self.XOModel = ursina.Entity(model=Models.GetModelPath("XOLogo"), scale=10)
        ursina.camera.position = self.ROOTCAMERAPOS
        ursina.camera.rotation = self.ROOTCAMERAROT
        self.Water.position = self.Water.position + (0,-1.1,0)
        
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
        #ursina.destroy(self.Trees)
        STATES["IN_MENU"] = False


class ThreeXThreeBoardScene():
    def __init__(self) -> None:
        pass

    def __del__(self):
        pass

    def onUpdate(self):
        pass