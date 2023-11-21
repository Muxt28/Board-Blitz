from json import load

AssetsFolder = "Assets\\"
ModelsIndex = load(open(r".\src\Frontend\ModelsIndex.json"))
TextureIndex = load(open(r".\src\Frontend\TextureIndex.json"))

def GetModelPath(TYPE):
    return AssetsFolder+ModelsIndex[TYPE]

def GetTexture(TYPE):
    return AssetsFolder+TextureIndex[TYPE]