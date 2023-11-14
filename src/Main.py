# Main File for Board Blitz

# Frontend Written by Uzair
# Backend written by Muqsit
# AI written by Safwaan

# python src\main.py

import ursina
import ursina.shaders as shaders
import asyncio
import time
import InputHandler
import Models
import UserInterface

app = ursina.Ursina (
    title = "Board Blitz",
    borderless = False,
    icon = ".\\Assets\\Logo.ico"
)

# Optimise input
ursina.window.fullscreen = False
ursina.window.exit_button.visible = False
ursina.window.fps_counter.enabled = True
ursina.window.forced_aspect_ratio = (16/9)

ursina.Sky()
CameraPosition = (0,20,-25)
CameraRotation = (40,0,0)

ursina.camera.orthographic = False
ursina.camera.fov = 90
ursina.camera.position = CameraPosition
ursina.camera.rotation = CameraRotation

#// ENTITIES
Board = ursina.Entity(model=Models.GetModelPath("3x3"), shader=shaders.basic_lighting_shader, color=ursina.color.rgb(255, 226, 200))
SplashScreen = UserInterface.ShowLoadingSplash()
ursina.invoke(UserInterface.destroyEntity, SplashScreen, delay=4)
#ursina.invoke(InputHandler.SetInputState, "TrackingInput", True, delay=4)
print("yo")

#InputHandler.SetInputState("TrackingInput", True)

# updates every frame loop
def update():
    # if InputHandler.INPUT_STATES["TrackingInput"]: # It's more efficient to evaluate a single boolean than evaluating the length of the array
    #     InputHandler.HandleKeys(ursina.input_handler.held_keys)
    # if InputHandler.INPUT_STATES["TrackingMouse"]:
    #     InputHandler.HandleMouse(ursina.input_handler.input())
    pass

def input(key):
    if InputHandler.GetInputState("TrackingInput"): # It's more efficient to evaluate a single boolean than evaluating the length of the array
        InputHandler.HandleKeys(key)
    if InputHandler.GetInputState("TrackingMouse"):
        InputHandler.HandleMouse(key)

#UI.MainMenu()
app.run()