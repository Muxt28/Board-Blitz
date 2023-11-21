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
import math
from Frontend import (
    GameManager,
    InputHandler,
    Models,
    UserInterface
)

app = ursina.Ursina (
    title = "Board Blitz",
    borderless = False,
    icon = r".\Assets\Logo.ico",
)

window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False
window.forced_aspect_ratio = (16/9)

ursina.Sky()
ursina.camera.orthographic = False
ursina.camera.fov = 90
ursina.camera.position = (0,0,0)
ursina.camera.rotation = (0,0,0)

DEBUG_MODE = True
DELAY_GL = 4 if (DEBUG_MODE!=True) else 0
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingMouse", True, delay=DELAY_GL)

GameManager.MENU_GLOBAL = GameManager.Menu((not DEBUG_MODE))
#GameManager.BOARD_SCENE_GLOBAL = GameManager.ThreeXThreeBoardScene()


def update():
    if GameManager.STATES["IN_MENU"]:
            GameManager.MENU_GLOBAL.onUpdate()
    if GameManager.STATES["In3x3Single"] or GameManager.STATES["In3x3Multiplayer"]:
            camera.position = (0,200,-230)
            camera.rotation = (45,0,0)
            camera.look_at = ursina.Vec3(0,0,0)

def input(key):
    if InputHandler.GetInputState("TrackingInput"):
        pass

    if InputHandler.GetInputState("TrackingMouse"):
        if GameManager.STATES["In3x3Single"] or GameManager.STATES["In3x3Multiplayer"]:
            InputHandler.HandleMouse(key)
            if key=="left mouse down":
                 GameManager.BOARD_SCENE_GLOBAL.handleMouseClick(mouse.world_point)
                 pass
                
app.run()