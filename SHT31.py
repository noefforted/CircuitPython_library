import time
import board
import busio

class SHT31:
    def __init__(self, i2c_bus=None, address=0x44):
        if i2c_bus is None:
            i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.i2c_bus = i2c_bus
        self.address = address

    def reset(self):
        """Mengirim perintah reset ke sensor"""
        self._send_command(0x30A2)
    
    def read_temperature_humidity(self):
        """Membaca suhu dan kelembapan dari sensor"""
        data = self._send_command(0x2C06, read_length=6)
        
        if data is None:
            return None, None
        
        temp_raw = (data[0] << 8) | data[1]
        humidity_raw = (data[3] << 8) | data[4]

        if not self._check_crc(data[:2], data[2]) or not self._check_crc(data[3:5], data[5]):
            return None, None

        temperature = -45 + (175 * (temp_raw / 65535.0))
        humidity = 100 * (humidity_raw / 65535.0)
        
        return temperature, humidity

    def _send_command(self, command, read_length=0):
        """Mengirim perintah I2C ke sensor dan membaca data jika perlu"""
        try:
            self.i2c_bus.writeto(self.address, bytearray([(command >> 8) & 0xFF, command & 0xFF]))
            if read_length > 0:
                result = bytearray(read_length)
                self.i2c_bus.readfrom_into(self.address, result)
                return result
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _check_crc(self, data, checksum):
        """Menghitung CRC8 dan membandingkannya dengan checksum yang diterima"""
        crc = self._crc8(data)
        return crc == checksum
    
    def _crc8(self, data):
        """Menghitung CRC8 menggunakan algoritma polynomial 0x31"""
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
        return crc & 0xFF
