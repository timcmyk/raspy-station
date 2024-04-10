# Module Imports
from datetime import datetime
import firebase_admin
from firebase_admin import db, credentials
from initialization.json_helper import getDictionaryFromJson


class DatabaseService:
    def __init__(self):
        self.connect()

    def connect(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("../../credentials.json")
            firebase_admin.initialize_app(
                cred,
                {
                    "databaseURL": "https://raspy-station-default-rtdb.europe-west1.firebasedatabase.app"
                },
            )

    # method to persist data entry
    def saveDataEntry(self, sensorId, data):
        # do execute
        # get ownerId from owner file
        ownerDictionary = getDictionaryFromJson("../target/owner.json")
        ownerId = ownerDictionary.get("ownerId")
        dataEntryDictionary = {
            "data": data,
            "timestamp": datetime.timestamp(datetime.now()),
        }
        db.reference("/" + str(ownerId) + "/sensors/" + str(sensorId) + "/data").push(
            dataEntryDictionary
        )

    # method to persist owner (saves name and returns generated id)
    def createOwner(self, name, ownerId, dictionary):
        print("Trying to save owner with name: " + name)
        # do execute
        db.reference("/" + str(ownerId)).set(dictionary)
        return str(ownerId)

    # method to persist raspy (saves name and ownerId and returns generated id)
    def saveRaspies(self, ownerId, dictionary):
        print("Trying to save raspies for owner with id: " + str(ownerId))
        # do execute
        db.reference("/" + str(ownerId) + "/raspies").set(dictionary)
        return str(ownerId)

    def saveSensors(self, ownerId, dictionary):
        print("Trying to save sensors")
        # do execute
        db.reference("/" + str(ownerId) + "/sensors").set(dictionary)
        return str(ownerId)
