import fire

import os
import sys
import inspect

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
    dictionary = {"name": name}
    writeToJson(dictionary, fileName)


# command to save owner
def save():
    dictionary = getDictionaryFromJson(fileName)
    name = dictionary.get("name")
    ownerId = dictionary.get("ownerId")
    # check if name is set
    if name is None or name == "":
        print("Please set a name first by starting 'owner.py name'.")
    # check if owner has already been created
    elif ownerId is not None:
        print("Owner already saved. Trying to update the name")
        databaseService.connect()
        databaseService.updateOwner(ownerId, name)
    # create new owner
    else:
        databaseService.connect()
        ownerId = databaseService.createOwner(name)
        writeToJson({"ownerId": ownerId}, fileName)


if __name__ == "__main__":
    fire.Fire({"name": name, "save": save})
