import ursina
from time import sleep

def ShowLoadingSplash():
    BlackScreen = ursina.Entity(
        parent = ursina.camera.ui, 
        model = 'cube',
        scale = (2,2),                                           
        origin = (0,0),                                         
        position = (0,0),                                                                                                             
        color = ursina.color.black 
    )
    LogoImage = ursina.Entity(
        model = 'cube',
        parent = BlackScreen,
        scale = (.2,.2),
        position = (0,0.12),
        texture=".\\Assets\\LogoTrsprnt.png",
        alpha = 1,
    )
    b = ursina.Text(text='Board Blitz\nMade by Uzair, Muqsit & Safwaan', color=ursina.color.white, size=10,origin = (0,.5), parent = BlackScreen)
    b.default_resolution = 1080 * b.size
    return BlackScreen

def showEndScreen(TYPE):
    messages={
        "DRAW" : "You had a Draw!",
        "WIN" : "You won! Good game!",
        "LOSE" : "Your Opponent has won"
        "P1" : "Player 1 has won"
        "P2" : "Player 2 has won"
    }

    BlackScreen = ursina.Entity(
        parent = ursina.camera.ui,
        model = 'cube',
        scale = (2,2),                                           
        origin = (0,0),                                         
        position = (0,0),                                                                                                             
        color = ursina.color.black 
    )
    b = ursina.Text(text=messages[TYPE], color=ursina.color.white, size=10,origin = (0,.5), parent = BlackScreen)
    b.default_resolution = 1080 * b.size


def destroyEntity(ent):
    ursina.destroy(ent)

def MainMenu():
    pass
