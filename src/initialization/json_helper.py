import json
import os
from pathlib import Path


def writeToJson(newDictionary, fileName):
    # try to read old (existing) dictionary from json file
    oldDictionary = getDictionaryFromJson(fileName=fileName)
    if oldDictionary is None:
        oldDictionary = {}
    # merge old and new dictionary
    updatedDictionary = {**oldDictionary, **newDictionary}
    # Serializing json
    json_object = json.dumps(updatedDictionary)

    # Writing to sample.json
    with open("./target/" + fileName, "w") as outfile:
        outfile.write(json_object)


def getDictionaryFromJson(fileName):
    my_file = Path("./target/" + fileName)
    # check if file exists
    if my_file.is_file():
        # Opening JSON file
        with open("./target/" + fileName, "r") as openfile:
            # Reading from json file
            return json.load(openfile)


def changeFileName(oldName, newName):
    my_file = Path("./target/" + oldName)
    # check if file exists
    if my_file.is_file():
        os.rename("./target/" + oldName, "./target/" + newName)
    else:
        print("File does not exist")
