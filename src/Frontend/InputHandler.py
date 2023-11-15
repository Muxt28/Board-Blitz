import ursina

from Frontend import GameManager

INPUT_STATES = {
    "TrackingInput" : False,
    "TrackingMouse" : False,
}

def GetInputState(TYPE):
    return INPUT_STATES[TYPE]

def SetInputState(TYPE, newEvaluation):
    INPUT_STATES[TYPE] = newEvaluation


def HandleKeys(key):
    pass

def HandleMouse(key):
    pass