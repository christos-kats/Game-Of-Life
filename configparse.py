import configparser
import os.path

def checkNumDict(validDict, checkDict):
    for key in validDict:
        if isinstance(checkDict[key], tuple) :
            if len(checkDict[key]) != validDict[key][0]:
                return False
            for item in checkDict[key]:
                if not(item >= validDict[key][1] and item <= validDict[key][2]):
                    return False
        else:
            if not(checkDict[key] >= validDict[key][0] and checkDict[key] <= validDict[key][1]):
                return False
    return True

def readConfig(configName):
    configDict = {}
    try:
        config = configparser.ConfigParser()
        config.read(configName)
    except:
        raise Exception(f"Configuration file {configName} not found or can't be read.")
    try:
        configDict["gridX"] = int(config["GRID_PROPERTIES"]["x"])
        configDict["gridY"] = int(config["GRID_PROPERTIES"]["y"])
        configDict["pixelSize"] = int(config["GRID_PROPERTIES"]["pixelSize"])
        configDict["randomChances"] = int(config["RANDOM_CHANCES"]["chances"])
        configDict["bgColor"] = tuple([ int(i) for i in config["COLORS"]["background"].split(",")])
        configDict["fgColor"] = tuple([ int(i) for i in config["COLORS"]["foreground"].split(",")])
        configDict["startingInterval"] = float(config["SPEED"]["startingInterval"])
        configDict["intervalLimits"] = tuple([float(i) for i in config["SPEED"]["intervalLimits"].split(",")])
        configDict["font"] = config["FONT"]["font"]
    except:
        raise Exception("Configuration File contains incorrect formatting.")
    validDict = {"gridX": (10, 200), "gridY": (10,200), "pixelSize": (5,20), "randomChances": (1,9), "bgColor":(3, 0, 255), "fgColor":(3, 0, 255), "intervalLimits": (2, 0.01, 10), "startingInterval": (configDict["intervalLimits"][0], configDict["intervalLimits"][1])}
    if not(checkNumDict(validDict, configDict)):
        raise Exception("Configuration file contains values out of range or incorrect formatting")
    if not(os.path.exists(configDict["font"])):
        raise Exception(f"Font file: {configDict['font']} does not exist")
    return configDict
