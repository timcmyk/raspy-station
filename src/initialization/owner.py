import fire

import os
import sys
import inspect
from datetime import datetime


# add parent directory to path to prepare for relative imports
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from initialization.json_helper import writeToJson, getDictionaryFromJson
from services.database_service import DatabaseService

databaseService = DatabaseService()

fileName = "owner.json"


# command to set name
def name(name):
    # take name and write it to json

    dictionary = getDictionaryFromJson(fileName)

    if dictionary is not None:
        oldName = dictionary.get("name")
        print("Name was already set to: " + oldName)
        print("Overwriting with new name: " + name)
        writeToJson({"name": name}, fileName)
    else:
        now = datetime.now()
        ownerId = id(now)
        dictionary = {"name": name, "ownerId": ownerId}
        writeToJson(dictionary, fileName)


# command to save owner
def save():
    dictionary = getDictionaryFromJson(fileName)
    name = dictionary.get("name")
    ownerId = dictionary.get("ownerId")
    # check if name is set
    if name is None or name == "":
        print("Please set a name first by starting 'owner.py name'.")
    # create or update owner
    else:
        databaseService.connect()
        databaseService.createOwner(name, ownerId, dictionary)


if __name__ == "__main__":
    fire.Fire({"name": name, "save": save})
