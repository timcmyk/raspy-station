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

fileFolder = "raspys/"
fileSuffix = "_raspy.json"


# command to set name
def name(name):
    # take name and write it to json
    dictionary = {"name": name}
    writeToJson(dictionary, fileFolder + name + fileSuffix)


# command to change name
def changeName(oldName, newName):
    # ensure that old file exists
    if checkIfRaspyFileAlreadyExists(oldName):
        dictionary = getDictionaryFromJson(fileFolder + oldName + fileSuffix)
        # set new name in dictionary
        dictionary["name"] = newName
        # update dictionary in json file
        writeToJson(dictionary, fileFolder + oldName + fileSuffix)
        # change file name to new name
        changeFileName(
            fileFolder + oldName + fileSuffix, fileFolder + newName + fileSuffix
        )
    else:
        printHint(name)


# command to set ownerId
def owner(name, ownerId):
    # take ownerId and write it to json
    dictionary = {"ownerId": ownerId}
    # can only be done if raspy file already exists
    if checkIfRaspyFileAlreadyExists(name):
        writeToJson(dictionary, fileFolder + name + fileSuffix)
    else:
        printHint(name)


# command to save all raspys
def saveAll():
    raspyDirectory = "./target/" + fileFolder
    # iterate over files in raspy directory
    for filename in os.listdir(raspyDirectory):
        f = os.path.join(raspyDirectory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            saveSingle(filename)


def saveSingle(filename):
    dictionary = getDictionaryFromJson(fileFolder + filename)
    name = dictionary.get("name")
    ownerId = dictionary.get("ownerId")
    raspyId = dictionary.get("raspyId")
    # check if name and ownerId are set
    if name is None or name == "":
        print("Name has to be set for raspy " + filename)
    elif ownerId is None or ownerId == "":
        print("Owner has to be set for raspy " + filename)
    # check if raspy has already been created -> update name
    elif raspyId is not None:
        print("Raspy already saved. Trying to update the name")
        databaseService.connect()
        databaseService.updateRaspyName(raspyId, name)
    # persist new raspy
    else:
        databaseService.connect()
        raspyId = databaseService.createRaspy(name, ownerId)
        writeToJson({"raspyId": raspyId}, fileFolder + filename)


def checkIfRaspyFileAlreadyExists(name):
    # is the file existing?
    return getDictionaryFromJson(fileFolder + str(name) + fileSuffix) is not None


def printHint(name):
    print(
        "Raspy file for raspy ",
        name,
        " does not exist. Please create it first by starting 'raspy.py name <name>'.",
    )


if __name__ == "__main__":
    fire.Fire({"name": name, "owner": owner, "save": saveAll, "changeName": changeName})
