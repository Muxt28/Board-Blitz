# Main File for Board Blitz

# Frontend Written by Uzair
# Backend written by Muqsit
# AI written by Safwaan
#############################
import ursina
import ursina.shaders as shaders
import ursina.mouse as mouse
import ursina.camera as camera 
import ursina.window as window

from Frontend import (
    GameManager,
    InputHandler,
    Models,
    UserInterface
)
#import Frontend.GameManager
#import Frontend.InputHandler
#import Frontend.Models
#import Frontend.UserInterface

app = ursina.Ursina (
    title = "Board Blitz",
    borderless = False,
    icon = ".\\Assets\\Logo.ico"
)

# Optimise input
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.forced_aspect_ratio = (16/9)

ursina.Sky()
##CameraPosition = (0,20,-25)
##CameraRotation = (40,0,0)

ursina.camera.orthographic = False
ursina.camera.fov = 90
ursina.camera.position = (0,0,0)
ursina.camera.rotation = (0,0,0)

#Board = ursina.Entity(model=Models.GetModelPath("3x3"), shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200))
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=4)
#ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=4)
ursina.invoke(InputHandler.SetInputState, "TrackingMouse", True, delay=4)

ROOTCAMERAPOS = (8,3.5,3.4)
ROOTCAMERAROT = (0,-130,0)
maxTilt = 10
def update():
    if GameManager.STATES["IN_MENU"]:
        x, y, z = mouse.position
        #print(ROOTCAMERAPOS)
        camera.position = ROOTCAMERAPOS + (-x*.1,y*.1,0)
        camera.rotation = ROOTCAMERAROT + (
            ((((y*150)-window.size.y/2)/window.size.y)*-maxTilt),
            ((((-x*150)-window.size.x/2)/window.size.x)*-maxTilt),
            0,
        )

def input(key):
    if InputHandler.GetInputState("TrackingInput"):
        InputHandler.HandleKeys(key)
    if InputHandler.GetInputState("TrackingMouse"):
        if key=="mouse":
            InputHandler.HandleMouse(key)

#MainMenuScene = ursina.load_model(name = "PalmTree.blend", path=ursina.Path(r".\\Assets\\Palm Tree\\proj_palmtree"))
MainScene = ursina.Entity(model=Models.GetModelPath("Beach"), scale=10, texture = Models.GetTexture("Beach"), shader=shaders.basic_lighting_shader)
Water = ursina.Entity(model=Models.GetModelPath("Water"), scale=10, texture = Models.GetTexture("Water"), shader=shaders.basic_lighting_shader)
Trees = ursina.Entity(model=Models.GetModelPath("Trees"), scale=10)
GameManager.STATES["IN_MENU"] = True
ursina.camera.position = (8,3.5,3.4)
ursina.camera.rotation = (0,-130,0)
#UI.MainMenu()
app.run()