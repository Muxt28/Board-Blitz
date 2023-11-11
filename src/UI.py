from ursina import (
    Entity,
    camera,
    color
)

def ShowLoadingSplash():
    BlackScreen = Entity(
        parent = camera.ui,
        model = 'cube',
        scale = (1, 1),                                           
        origin = (0,0),                                         
        position = (0,0),                                                                                                             
        color = color.black 
    )

    pass

def MainMenu():
    pass
