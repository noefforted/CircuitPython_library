import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

class A02YYUW:
    def __init__(self, i2c, address=0x57):
        self.i2c_device = I2CDevice(i2c, address)
        self.buffer = bytearray(3)  # Untuk menyimpan data dari sensor

    def _read_data(self):
        with self.i2c_device as i2c:
            i2c.readinto(self.buffer)
        # Buffer berisi 3 byte data
        return self.buffer

    def get_distance(self):
        """Membaca jarak dari sensor dalam cm"""
        data = self._read_data()
        # Data jarak disimpan dalam dua byte pertama
        distance = (data[0] << 8) | data[1]
        return distance

    def get_checksum(self):
        """Membaca checksum dari byte terakhir"""
        data = self._read_data()
        return data[2]

    def validate_data(self):
        """Validasi data menggunakan checksum sederhana"""
        data = self._read_data()
        checksum = (data[0] + data[1]) & 0xFF
        return checksum == data[2]

# Example of usage
i2c = busio.I2C(board.SCL, board.SDA)
sensor = A02YYUW(i2c)

while True:
    if sensor.validate_data():
        distance = sensor.get_distance()
        print(f"Distance: {distance} cm")
    else:
        print("Data not valid")
    time.sleep(1)
