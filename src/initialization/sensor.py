import fire
import os
import sys
import inspect

from datetime import datetime


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

fileName = "sensor.json"


# command to set address
# -> has to be set first (works as local identifier unless it is not used or persisted yet)
def sensor(name, address, raspyId, unit, highestPossible, lowestPossible):
    # get ownerId from owner file
    ownerDictionary = getDictionaryFromJson("../target/owner.json")
    ownerId = ownerDictionary.get("ownerId")
    print("Owner recognized with id: " + str(ownerId))
    dictionary = getDictionaryFromJson(fileName)

    # check if file already exists
    if dictionary is not None:
        sensors = dictionary["sensors"]
        print(sensors)
        print("Totally found " + str(sensors.__len__()) + " Sensor(s)")
        print("Adding new sensor with address : " + str(address))
        newSensorDictionary = {
            id(datetime.now()): {
                "sensorId": id(datetime.now()),
                "name": name,
                "address": address,
                "rasypId": raspyId,
                "unit": unit,
                "highestPossible": highestPossible,
                "lowestPossible": lowestPossible,
            }
        }
        print(sensors)
        newDictionary = {"sensors": {**sensors, **newSensorDictionary}}

        writeToJson(newDictionary, fileName)
    else:
        dictionary = {
            "ownerId": ownerId,
            "sensors": {
                id(datetime.now()): {
                    "sensorId": id(datetime.now()),
                    "name": name,
                    "address": address,
                    "rasypId": raspyId,
                    "unit": unit,
                    "highestPossible": highestPossible,
                    "lowestPossible": lowestPossible,
                }
            },
        }
        writeToJson(dictionary, fileName)


# command to save all sensors
def save():
    dictionary = getDictionaryFromJson(fileName)

    ownerId = dictionary.get("ownerId")
    databaseService.connect()
    databaseService.saveSensors(ownerId, dictionary.get("sensors"))


if __name__ == "__main__":
    fire.Fire(
        {
            "sensor": sensor,
            "save": save,
        }
    )
