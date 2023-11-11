# Main File for Board Blitz

# Frontend Written by Uzair
# Backend written by Muqsit

# python .\src\main.py
from ursina import (
    Ursina,
    window,
    Entity,
    input_handler,
    color,
    time, 
    Sky, 
    EditorCamera, 
    mesh_importer, 
    scene,
    DirectionalLight,
    PointLight,
    vec3,
    camera,
    mouse
)

from ursina.shaders import *
import UI
import Models

app = Ursina (
    title = "Board Blitz",
    borderless=False,
)

window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.forced_aspect_ratio = (16/9)

Sky()
CameraPosition = (0,20,-25)
CameraRotation = (40,0,0)

camera.orthographic = False
camera.fov = 90
camera.position = CameraPosition
camera.rotation = CameraRotation

#// ENTITIES
Board = Entity(model=Models.GetModelPath("3x3"), shader=basic_lighting_shader, color=color.rgb(255, 226, 200))
#pivot = Entity(rotation =(-45,0,0))
#Light = PointLight(parent=pivot, y=10, z=50, shadows=True)
#Cube = Entity(parent=Light, model='cube', size = (10,10,10))

# updates every frame loop
def update():
    pass

#UI.ShowLoadingSplash()
#UI.MainMenu()

app.run()