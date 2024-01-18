from dataclasses import dataclass

@dataclass
class Owner: 
    id: int
    name: str

@dataclass
class Raspy: 
    id: int
    name: str
    owner: Owner
    sensors: list

@dataclass
class Sensor:
    id: int
    name: str
    dataEntries: list
    isAvailable: bool
    unit: str
    highestPossible: int
    lowestPossible: int

@dataclass
class DataEntry:
    id: int
    value: int

