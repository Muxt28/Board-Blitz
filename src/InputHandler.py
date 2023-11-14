import ursina

INPUT_STATES = {
    "TrackingInput" : False,
    "TrackingMouse" : False,
}

def GetInputState(TYPE):
    return INPUT_STATES[TYPE]

def SetInputState(TYPE, newEvaluation):
    INPUT_STATES[TYPE] = newEvaluation


def HandleKeys(key):
    print(key)

def HandleMouse(key):
    print(key)