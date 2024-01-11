class Owner: 
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Raspy: 
    def __init__(self, id, name, owner, sensors):
        self.id = id
        self.name = name
        self.owner = owner
        self.sensors = sensors

class Sensor:
    def __init__(self, id, name, dataEntries, isAvailable, 
    unit, highestPossible, lowestPossible):
        self.id = id
        self.name = name
        self.dataEntries = dataEntries
        self.isAvailable = isAvailable
        self.unit = unit
        self.highestPossible = highestPossible
        self.lowestPossible = lowestPossible

class DataEntry:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp

