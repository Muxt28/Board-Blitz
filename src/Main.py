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

#
DEBUG_MODE = False
DELAY_GL = 4 #if DEBUG_MODE else 0
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingMouse", True, delay=DELAY_GL)

GameManager.MENU_GLOBAL = GameManager.Menu()
#GameManager.BOARD_SCENE_GLOBAL = GameManager.ThreeXThreeBoardScene()
def update():
    if GameManager.STATES["IN_MENU"]:
        # Camera stuff
            GameManager.MENU_GLOBAL.onUpdate()
    if GameManager.STATES["In3x3Single"]:
            camera.position = (10,10,10)
            GameManager.BOARD_SCENE_GLOBAL.onUpdate()

def input(key):
    if InputHandler.GetInputState("TrackingInput"):
        #InputHandler.HandleKeys(key)
        if key=="p": ## DEBUG
            GameManager.MENU_GLOBAL.destroy()
        if key=="m":
            GameManager.MENU_GLOBAL = GameManager.Menu(False)
    if InputHandler.GetInputState("TrackingMouse"):
        if key=="mouse":
            InputHandler.HandleMouse(key)

#UI.MainMenu()
app.run()