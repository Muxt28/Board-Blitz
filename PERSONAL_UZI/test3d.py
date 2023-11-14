from ursina import (
    Ursina, window, held_keys, Entity, color,
    time, Sky, EditorCamera
)

# updates every frame loop
def update():
    cube.rotation_y += time.dt * 100 
    cube.rotation_x += time.dt*50

app = Ursina (
    title = "Board Blitz",
    borderless=False   
)

window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

cube = Entity(model='cube', color=color.orange, scale=(2,2,2))
BasePlate=Entity(model='plane', color=color.gray, position=(0,-5,0), scale=10, rotation=(0,90,0))
newcube = Entity(parent=cube, model='cube', color=color.rgb(255, 0, 0), position=(3, 0, 0), scale=(1.5,1.5,1.5))

Sky()
EditorCamera()

app.run()