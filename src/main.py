# Originally from https://github.com/DFRobot/DFRobot_DHT20/tree/master/python/raspberrypi
# Modified by https://github.com/cjee21/ on 16 January 2023

from time import sleep

from services.aggregators.data_aggregator import DataAggregator
from services.database_service import DatabaseService

# The first  parameter is to select i2c0 or i2c1
# The second parameter is the i2c device address
I2C_BUS = 0x01  # default use I2C1 bus
I2C_ADDRESS = 0x38  # default I2C device address

dht20 = DataAggregator(I2C_BUS, I2C_ADDRESS)
databaseService = DatabaseService()

# Initialize sensor
if not dht20.begin():
    print("DHT20 sensor initialization failed")
else:
    # connect to database
    databaseService.connect()
    while True:
        # Read ambient temperature and relative humidity and print them to terminal
        T_celsius, humidity, crc_error = dht20.get_temperature_and_humidity()
        if crc_error:
            print("CRC               : Error\n")
        else:
            T_fahrenheit = T_celsius * 9 / 5 + 32

            # save in database
            # sensorIds have to be set manually for now
            databaseService.saveDataEntry(0, 0, T_celsius)
            databaseService.saveDataEntry(0, 1, humidity)

            sleep(300)
