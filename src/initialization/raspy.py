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

fileName = "raspy.json"


# command to set name
def name(name):

    # get ownerId from owner file
    ownerDictionary = getDictionaryFromJson("../target/owner.json")
    ownerId = ownerDictionary.get("ownerId")
    print("Owner recognized with id: " + str(ownerId))
    dictionary = getDictionaryFromJson(fileName)

    # check if file already exists
    if dictionary is not None:
        raspies = dictionary["raspies"]
        print(raspies)
        print("Totally found " + str(raspies.__len__()) + " Raspi(es)")
        print("Adding new raspy with name : " + name)
        raspies.append({"name": name, "raspyId": id(datetime.now())})
        print(raspies)
        newDictionary = {"raspies": raspies}

        writeToJson(newDictionary, fileName)
    else:
        now = datetime.now()
        raspyId = id(now)
        dictionary = {
            "ownerId": ownerId,
            "raspies": [{"name": name, "raspyId": raspyId}],
        }
        writeToJson(dictionary, fileName)


def save():
    dictionary = getDictionaryFromJson(fileName)
    ownerId = dictionary.get("ownerId")
    # check if name and ownerId are set
    if ownerId is None or ownerId == "":
        print("Owner has to be set first")
    # save new raspy or update existing one
    else:
        databaseService.connect()
        databaseService.saveRaspies(ownerId, dictionary.get("raspies"))


def printHint(name):
    print(
        "Raspy file for raspy ",
        name,
        " does not exist. Please create it first by starting 'raspy.py name <name>'.",
    )


if __name__ == "__main__":
    fire.Fire({"name": name, "save": save})
