import sys
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

from time import sleep

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
# GameManager.BOARD_SCENE_GLOBAL = GameManager.MultiplayerBoardScene()

BoxesFilled = 0
board = [['-'for _ in range(3)] for _ in range(3)]

def update():
    if GameManager.STATES["IN_MENU"]:
            GameManager.MENU_GLOBAL.onUpdate()
    if GameManager.STATES["In3x3Single"]:
            camera.position = (0,200,-230)
            camera.rotation = (45,0,0)
            camera.look_at = ursina.Vec3(0,0,0)

def input(key):
    global BoxesFilled, board
    if InputHandler.GetInputState("TrackingInput"):
        pass

    if InputHandler.GetInputState("TrackingMouse"):
        if GameManager.STATES["In3x3Single"]:
            InputHandler.HandleMouse(key)
            if key=="left mouse down":
                print(mouse.world_point)
                if mouse.world_point==None:
                     # player didnt touch the screen, ignore
                    return

                values, board = GameManager.BOARD_SCENE_GLOBAL.handleMouseClick(mouse.world_point, BoxesFilled, board)
                if values == 'NOT VALID':
                    GameManager.BOARD_SCENE_GLOBAL.StatusText = '*[ Move Not Valid ]*'
                    return
                
                BoxesFilled += 1
                # print(f'Boxes FIlled : {BoxesFilled}')
                if BoxesFilled == 9:
                    global app
                    UserInterface.showEndScreen("DRAW")
                    print('*[ Draw ]*')
                    #sys.exit()
                    ursina.invoke(sys.exit,delay=5)
                
                if values != None:
                    print(values)
                    MSG = ""
                    if values=="*[ You have Won ]*":
                        MSG = 'WIN'
                    elif values == '*[ Player 1 has Won ]*':
                        MSG = 'P1'
                    elif values == '*[ Player 2 has Won ]*':
                        MSG = 'P2'
                    elif values == '*[ Your opponent has won ]*':
                        MSG = 'LOSE'
                    
    
                         
                    UserInterface.showEndScreen(MSG)
                    ursina.invoke(sys.exit,delay=5)
                        
app.run()
