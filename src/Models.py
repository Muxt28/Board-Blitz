from json import load

AssetsFolder = "Assets\\"
ModelsIndex = load(open(r".\src\ModelsIndex.json"))

def GetModelPath(TYPE):
    return AssetsFolder+ModelsIndex[TYPE]
