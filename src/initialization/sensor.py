import fire
import os
import sys
import inspect

# add parent directory to path to prepare for relative imports
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from initialization.json_helper import (
    writeToJson,
    getDictionaryFromJson,
    changeFileName,
)
from services.database_service import DatabaseService

databaseService = DatabaseService()

fileFolder = "sensors/"
fileSuffix = "_sensor.json"


# command to set address
# -> has to be set first (works as local identifier unless it is not used or persisted yet)
def address(address):
    # take address and write it to json
    dictionary = {"address": address}
    writeToJson(dictionary, fileFolder + str(address) + fileSuffix)


# command to change address
def changeAddress(oldAddress, newAddress):
    # ensure that old file exists
    if checkIfSensorFileAlreadyExists(oldAddress):
        dictionary = getDictionaryFromJson(fileFolder + str(oldAddress) + fileSuffix)
        # set new address in dictionary
        dictionary["address"] = newAddress
        # update dictionary in json file
        writeToJson(dictionary, fileFolder + str(oldAddress) + fileSuffix)
        # change file name to new address
        changeFileName(
            fileFolder + str(oldAddress) + fileSuffix,
            fileFolder + str(newAddress) + fileSuffix,
        )
    else:
        printHint(name)


# command to set raspyId
def raspyId(address, raspyId):
    # take raspyId and write it to json
    dictionary = {"raspyId": raspyId}
    applyValue(address, dictionary)


# command to set name
def name(address, name):
    # take name and write it to json
    dictionary = {"name": name}
    applyValue(address, dictionary)


# command to set unit
def unit(address, unit):
    # take unit and write it to json
    dictionary = {"unit": unit}
    applyValue(address, dictionary)


# command to set highestPossible value
def highestPossible(address, highestPossible):
    # take highestPossible and write it to json
    dictionary = {"highestPossible": highestPossible}
    applyValue(address, dictionary)


# command to set lowestPossible value
def lowestPossible(address, lowestPossible):
    # take lowestPossible and write it to json
    dictionary = {"lowestPossible": lowestPossible}
    applyValue(address, dictionary)


# gets called when command save is executed
# -> saves (creates or updates) all raspys
# when they meet the requirements (every field is set)
def saveAll():
    raspyDirectory = "./target/" + fileFolder
    # iterate over files in sensor directory
    for filename in os.listdir(raspyDirectory):
        f = os.path.join(raspyDirectory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            saveSingle(filename)


# saves (creates or updates) a single sensor
def saveSingle(filename):
    # getting all attributes from json file
    dictionary = getDictionaryFromJson(fileFolder + filename)
    sensorId = dictionary.get("sensorId")
    raspyId = dictionary.get("raspyId")
    name = dictionary.get("name")
    unit = dictionary.get("unit")
    highestPossible = dictionary.get("highestPossible")
    lowestPossible = dictionary.get("lowestPossible")
    # check if everything is set
    if name is None or name == "":
        print("Name has to be set for sensor " + filename)
    elif raspyId is None or raspyId == "":
        print("Raspy has to be set for sensor " + filename)
    elif unit is None or unit == "":
        print("Unit has to be set for sensor " + filename)
    elif highestPossible is None or highestPossible == "":
        print("Highest possible value has to be set for sensor " + filename)
    elif lowestPossible is None or lowestPossible == "":
        print("Lowest possible value has to be set for sensor " + filename)
    # check if sensor has already been created -> update it
    elif sensorId is not None:
        print("Sensor already saved. Trying to update the name")
        databaseService.connect()
        databaseService.updateSensor(
            sensorId=sensorId,
            name=name,
            unit=unit,
            highestPossible=highestPossible,
            lowestPossible=lowestPossible,
        )
    # persist new sensor
    else:
        databaseService.connect()
        sensorId = databaseService.createSensor(
            name=name,
            raspyId=raspyId,
            unit=unit,
            highestPossible=highestPossible,
            lowestPossible=lowestPossible,
        )
        writeToJson({"sensorId": sensorId}, fileFolder + filename)


def applyValue(address, dictionary):
    if checkIfSensorFileAlreadyExists(address):
        writeToJson(dictionary, fileFolder + str(address) + "_sensor.json")
    else:
        printHint(address)


def checkIfSensorFileAlreadyExists(address):
    if getDictionaryFromJson(fileFolder + str(address) + "_sensor.json") is None:
        return False
    else:
        return True


def printHint(address):
    print(
        "Sensor file with address ",
        address,
        " does not exist. Please create it first by starting 'sensor.py address'.",
    )


if __name__ == "__main__":
    fire.Fire(
        {
            "address": address,
            "raspyId": raspyId,
            "changeAddress": changeAddress,
            "name": name,
            "unit": unit,
            "highestPossible": highestPossible,
            "lowestPossible": lowestPossible,
            "save": saveAll,
        }
    )
