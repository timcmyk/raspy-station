# Module Imports
import mariadb
import sys


class DatabaseService:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user="raspy",
                password="Altemeißnerlandstraße39",
                host="192.168.2.149",
                port=3307,
                database="raspystation_db",
            )
            # set connection and cursor to class variables
            self.conn = conn
            self.cursor = conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    # method to persist data entry
    def saveDataEntry(self, sensorId, data):
        # do execute
        sql = "INSERT INTO raspystation_db.DataEntry (sensorId, value) VALUES (?, ?)"
        self.cursor.execute(
            sql,
            (
                sensorId,
                data,
            ),
        )
        self.conn.commit()

    # method to persist owner (saves name and returns generated id)
    def createOwner(self, name):
        print("Trying to save owner with name: " + name)
        # do execute
        sql = "INSERT INTO raspystation_db.Owner (name) VALUES (?)"
        self.cursor.execute(sql, (name,))
        self.conn.commit()
        # get generated id
        ownerId = self.cursor.lastrowid
        self.closeDbConnection()
        return ownerId

    def updateOwner(self, ownerId, name):
        print("Trying to update owner with id: " + str(ownerId) + " and name: " + name)
        # do execute
        sql = "UPDATE raspystation_db.Owner SET name = ? WHERE id = ?"
        self.cursor.execute(
            sql,
            (
                name,
                ownerId,
            ),
        )
        self.conn.commit()
        self.closeDbConnection()

    # method to persist raspy (saves name and ownerId and returns generated id)
    def createRaspy(self, name, ownerId):
        sql = "INSERT INTO raspystation_db.Raspy (name, ownerId) VALUES (?, ?)"
        self.cursor.execute(
            sql,
            (
                name,
                ownerId,
            ),
        )
        self.conn.commit()
        raspyId = self.cursor.lastrowid
        self.closeDbConnection()
        return raspyId

    # method to update raspy's name
    def updateRaspyName(self, raspyId, name):
        sql = "UPDATE raspystation_db.Raspy SET name = ? WHERE id = ?"
        self.cursor.execute(
            sql,
            (
                name,
                raspyId,
            ),
        )
        self.conn.commit()
        self.closeDbConnection()

    def createSensor(self, name, raspyId, unit, highestPossible, lowestPossible):
        sql = "INSERT INTO raspystation_db.Sensor (name, raspyId, unit, highestPossible, lowestPossible) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(
            sql,
            (
                name,
                raspyId,
                unit,
                highestPossible,
                lowestPossible,
            ),
        )
        self.conn.commit()
        sensorId = self.cursor.lastrowid
        self.closeDbConnection()
        return sensorId

    def updateSensor(self, sensorId, name, unit, highestPossible, lowestPossible):
        sql = "UPDATE raspystation_db.Sensor SET name = ?, unit = ?, highestPossible = ?, lowestPossible = ? WHERE id = ?"
        self.cursor.execute(
            sql,
            (
                name,
                unit,
                highestPossible,
                lowestPossible,
                sensorId,
            ),
        )
        self.conn.commit()
        self.closeDbConnection()

    def closeDbConnection(self):
        self.cursor.close()
        self.conn.close()
