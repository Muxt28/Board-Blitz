from ursina import (
    Ursina, window, held_keys, Entity, color,
    time, Sky, EditorCamera, mesh_importer
)

# updates every frame loop
def update():
    pass

app = Ursina (
    title = "Board Blitz",
    borderless=False   
)

window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

BoardModelReference = mesh_importer.load_model("FixedBoard.obj")
BoardModelEntity = Entity(model=BoardModelReference)

Sky()
EditorCamera()

app.run()