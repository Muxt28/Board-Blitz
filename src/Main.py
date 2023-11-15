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

#Board = ursina.Entity(model=Models.GetModelPath("3x3"), shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200))
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=4)
ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=4)
ursina.invoke(InputHandler.SetInputState, "TrackingMouse", True, delay=4)

Menu = GameManager.Menu()

def update():
    if GameManager.STATES["IN_MENU"]:
        # Camera stuff
            Menu.onUpdate()

def input(key):
    if InputHandler.GetInputState("TrackingInput"):
        #InputHandler.HandleKeys(key)
        if key=="p": ## DEBUG
            global Menu
            del Menu
        if key=="m":
            Menu = GameManager.Menu()
    if InputHandler.GetInputState("TrackingMouse"):
        if key=="mouse":
            InputHandler.HandleMouse(key)

#UI.MainMenu()
app.run()