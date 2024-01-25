
class HumidityAggregator:
    
    def calculateHumidity(data):
        humidity_rawData = ((data[3] & 0xf0) >> 4) + (data[1] << 12) + (data[2] << 4)
        humidity = float(humidity_rawData) / 0x100000 * 100
        return humidity