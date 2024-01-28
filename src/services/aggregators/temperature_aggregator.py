class TemperatureAggregator:
    def calculateTempreature(data):
        temperature_rawData = ((data[3] & 0xF) << 16) + (data[4] << 8) + data[5]
        temperature = float(temperature_rawData) / 5242.88 - 50
        return temperature
