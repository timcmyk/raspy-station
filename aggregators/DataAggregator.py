# -*- coding: utf-8 -*

# Originally from https://github.com/DFRobot/DFRobot_DHT20/tree/master/python/raspberrypi
#
# Modified by https://github.com/cjee21/
# MIT License
# Copyright (c) 2022-2023 cjee21
# 
#
# Modifications:
#
# 25 February 2022
# - use smbus2
# - add decimal to temperature formula
# - add get_temperature_and_humidity function for getting temperature and humidity in a single read
#
# 16 January 2023
# - correct sensor initialization check and clean up init (begin) function
# - improve get_temperature_and_humidity function
# - add CRC-8 checking
# - remove functions no longer needed
# - add debug logging
# Note: Sensor initialization and CRC-8 calculation is based on Aosong sample code from
#       http://aosong.com/userfiles/files/software/AHT20-21%20DEMO%20V1_3(1).rar

"""
  *@file DFRobot_DHT20.py
  *@brief Define the basic structure of class DFRobot_DHT20
  *@copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  *@licence     The MIT License (MIT)
  *@author [fengli](li.feng@dfrobot.com)
  *@version  V1.0
  *@date  2021-6-25
  *@get from https://www.dfrobot.com
  *@https://github.com/DFRobot/DFRobot_DHT20
"""

import time
import smbus2 as smbus
import logging
from TemperatureAggregator import TemperatureAggregator
from HumidityAggregator import HumidityAggregator

# debug logging
logging.basicConfig()
logger = logging.getLogger(__name__)
# uncomment line below this to enable debug logging
#logger.setLevel(logging.DEBUG)
                
class DFRobot_DHT20(object):

  ''' Conversion data '''

  _DEFAULT_ADDRESS = 0x50
  _INIT_REG = 0x71
  _TRIGGER_REG = 0xac
  _DATA_REG = 0x71
  _TRIGGER_COMMAND = [0x33, 0x00]
  _CRC_POLYNOMIAL = 0x31


  def __init__(self, bus, address=_DEFAULT_ADDRESS):
        self.i2cbus = smbus.SMBus(bus)
        self._addr = address
        self.idle = 0


  # Sensor initialization function
  # @return Return True if initialization succeeds, otherwise return False.
  def begin(self):
        # after power-on, wait no less than 100ms
        time.sleep(0.5)

        # check and return initialization status
        data = self.read_reg(self._INIT_REG, 1)
        return (data[0] & 0x18) == 0x18


  # Get both temperature and humidity in a single read
  # @return Return temperature (C), humidity (%) and CRC result (True if error else False) as tuple
  def get_temperature_and_humidity(self):
        # trigger measurement
        self.write_reg(self._TRIGGER_REG, self._TRIGGER_COMMAND)

        # wait 80 ms and keep waiting until the measurement is completed
        while True:
            time.sleep(0.08)
            data = self.read_reg(self._DATA_REG, 1)
            if (data[0] & 0x80) == 0:
                break

        # read sensor data
        data = self.read_reg(self._DATA_REG, 7)

        # extract and convert temperature and humidity from data
        temperature = TemperatureAggregator.calculateTempreature(data)
        humidity = HumidityAggregator.calculateHumidity(data)

        # check CRC
        crc_error = self.calc_CRC8(data) != data[6]

        # debug logging
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Raw data      : 0x{''.join(format(x, '02x') for x in data)}")
            logger.debug(f"Read CRC      : {hex(data[6])}")
            logger.debug(f"Calculated CRC: {hex(self.calc_CRC8(data))}")
            logger.debug(f"Temperature   : {temperature}°C")
            logger.debug(f"Humidity      : {humidity}%")

        # return results
        return (temperature, humidity, crc_error)


  # CRC function
  # @param message - data from sensor which its CRC-8 is to be calculated
  # @return Return calculated CRC-8
  def calc_CRC8(self, data):
        crc = 0xFF
        for i in data[:-1]:
            crc ^= i
            for _ in range(8):
                crc = (crc << 1) ^ self._CRC_POLYNOMIAL if crc & 0x80 else crc << 1
        return crc & 0xFF

  
  def write_reg(self, reg, data):
        time.sleep(0.01)
        self.i2cbus.write_i2c_block_data(self._addr, reg, data)
  
  
  def read_reg(self, reg, length):
        time.sleep(0.01)
        return self.i2cbus.read_i2c_block_data(self._addr, reg, length)