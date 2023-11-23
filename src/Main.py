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
from multiprocessing.pool import ThreadPool

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

DEBUG_MODE = False
DELAY_GL = 4 if (DEBUG_MODE!=True) else 0
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=DELAY_GL)
ursina.invoke(InputHandler.SetInputState, "TrackingMouse", True, delay=DELAY_GL)

GameManager.MENU_GLOBAL = GameManager.Menu((not DEBUG_MODE))
# GameManager.BOARD_SCENE_GLOBAL = GameManager.AIBoardScene()
# GameManager.BOARD_SCENE_GLOBAL.setStatusText = 'CLick Anywhere to start'

BoxesFilled = 0
board = [['-'for _ in range(3)] for _ in range(3)]
start = False
Valid_Coordinates = ['00', '01', '02', '10', '11', '12', '20', '21', '22']

def update():
    if GameManager.STATES["IN_MENU"]:
            GameManager.MENU_GLOBAL.onUpdate()
    else:
    #if GameManager.STATES["In3x3Single"] or GameManager.STATES["In3x3Multiplayer"]:
            camera.position = (0,200,-230)
            camera.rotation = (45,0,0)
            camera.look_at = ursina.Vec3(0,0,0)

def input(key):
    global BoxesFilled, board, start
    if InputHandler.GetInputState("TrackingInput"):
        pass

    if InputHandler.GetInputState("TrackingMouse"):
        if GameManager.STATES["In3x3Single"] or GameManager.STATES["In3x3Multiplayer"] or GameManager.STATES["AIScene"]:
            InputHandler.HandleMouse(key)
            if key=="left mouse down":
                print(mouse.world_point)
                if mouse.world_point==None:
                     # player didnt touch the screen, ignore
                    return
                
                if start == False and GameManager.BOARD_SCENE_GLOBAL.__class__.__name__ == 'MultiplayerBoardScene':
                    start = True
                    values = GameManager.BOARD_SCENE_GLOBAL.receive()

                elif GameManager.BOARD_SCENE_GLOBAL.__class__.__name__ == 'AIBoardScene':
                        sent = False
                        while not sent:
                            values, board, BoxesFilled = GameManager.BOARD_SCENE_GLOBAL.handleMouseClick(mouse.world_point, BoxesFilled, board, Valid_Coordinates)
                            if values != 'NEED COORDIANTES':
                                sent = True
                            else:
                                values, board, BoxesFilled = GameManager.BOARD_SCENE_GLOBAL.handleMouseClick(mouse.world_point, BoxesFilled, board, Valid_Coordinates)
        
                elif GameManager.BOARD_SCENE_GLOBAL.__class__.__name__ == 'ThreeXThreeBoardScene':
                    values, BoxesFilled = GameManager.BOARD_SCENE_GLOBAL.handleMouseClick(mouse.world_point, BoxesFilled, board)
                
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

                if values == 'NO WIN':
                    pass
                
                elif values != None:
                    print(values)
                    MSG = ""
                    if values=="*[ You have Won ]*":
                        MSG = 'WIN'
                    elif values == '*[ Player 1 has Won ]*':
                        MSG = 'P1'
                    elif values == '*[ Player 2 has Won ]*':
                        MSG = 'P2'
                    elif values == '*[ Your opponent has won ]*' or values == '*[ AI has won ]*':
                        MSG = 'LOSE'
                    elif values == 'DRAW':
                        global app
                        UserInterface.showEndScreen("DRAW")
                        ursina.invoke(sys.exit,delay=5)                    
                         
                    UserInterface.showEndScreen(MSG)
                    ursina.invoke(sys.exit,delay=5)
                        
app.run()
