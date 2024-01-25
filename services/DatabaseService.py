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
            self.conn = conn
            self.cursor = conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def saveTemperature(self, sensorId, temperature):
        self.cursor.execute(
            "INSERT INTO raspystation_db.DataEntry (sensorId, value) VALUES (?, ?)",
            (
                sensorId,
                temperature,
            ),
        )
        self.conn.commit()

    def saveHumidity(self, sensorId, humidity):
        self.cursor.execute(
            "INSERT INTO raspystation_db.DataEntry (sensorId, value) VALUES (?, ?)",
            (
                sensorId,
                humidity,
            ),
        )
        self.conn.commit()
