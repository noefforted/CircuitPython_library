import time
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

class SHT31:
    def __init__(self, i2c, address=0x44):
        self.i2c_device = I2CDevice(i2c, address)
        self.buffer = bytearray(6)  # 6 byte buffer for SHT31 data

    def _send_command(self, command):
        """Mengirim command 2 byte ke sensor."""
        with self.i2c_device as i2c:
            i2c.write(bytes([command >> 8, command & 0xFF]))

    def _read_data(self):
        """Membaca 6 byte data dari sensor."""
        with self.i2c_device as i2c:
            i2c.readinto(self.buffer)
        return self.buffer

    def _calculate_temperature(self, temp_data):
        """Menghitung suhu dari 2 byte pertama."""
        raw_temperature = (temp_data[0] << 8) | temp_data[1]
        temperature = -45 + (175 * (raw_temperature / 65535.0))
        return temperature

    def _calculate_humidity(self, humidity_data):
        """Menghitung kelembapan dari 2 byte ketiga."""
        raw_humidity = (humidity_data[3] << 8) | humidity_data[4]
        humidity = 100 * (raw_humidity / 65535.0)
        return humidity

    def read_temperature_humidity(self):
        """Membaca dan mengembalikan suhu dan kelembapan."""
        self._send_command(0x2400)  # Perintah untuk pembacaan suhu dan kelembapan
        time.sleep(0.015)  # Tunggu 15ms untuk pengukuran
        data = self._read_data()

        # Periksa checksum
        if not self._check_crc(data[0:2], data[2]) or not self._check_crc(data[3:5], data[5]):
            raise RuntimeError("CRC check failed")

        temperature = self._calculate_temperature(data)
        humidity = self._calculate_humidity(data)
        return temperature, humidity

    def _check_crc(self, data, checksum):
        """Fungsi untuk memeriksa CRC8."""
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
        crc &= 0xFF
        return crc == checksum

# Contoh penggunaan
i2c = busio.I2C(board.SCL, board.SDA)
sensor = SHT31(i2c)

while True:
    try:
        temperature, humidity = sensor.read_temperature_humidity()
        print(f"Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} %")
    except RuntimeError as e:
        print(f"Error reading from sensor: {e}")
    time.sleep(2)
