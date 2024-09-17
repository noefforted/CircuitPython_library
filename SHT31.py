import time
import board
import busio

class SHT31:
    def __init__(self, i2c_address=0x44):
        """
        Inisialisasi sensor SHT31 menggunakan CircuitPython.
        """
        i2c = busio.I2C(board.SCL, board.SDA)  # Menggunakan SCL dan SDA bawaan
        self.i2c_device = i2c
        self.address = i2c_address
        self.command_measure = [0x2C, 0x06]  # Perintah untuk memulai pengukuran

    def send_command(self, command):
        """
        Mengirimkan perintah melalui I2C ke sensor SHT31.
        """
        self.i2c_device.writeto(self.address, bytes(command))

    def crc8(self, data):
        """
        Menghitung CRC-8 menggunakan polinomial 0x31 (CRC-8-CCITT).
        """
        polynomial = 0x31
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
                crc &= 0xFF  # Menjaga CRC tetap di 8 bit
        return crc

    def read_data(self):
        """
        Membaca data dari sensor setelah perintah pengukuran dikirim.
        Mengembalikan nilai suhu dan kelembaban yang dibaca dari sensor.
        """
        try:
            # Kirim perintah untuk memulai pengukuran
            self.send_command(self.command_measure)
            time.sleep(0.015)  # Tunggu pengukuran selesai (15ms)

            # Baca 6 byte dari sensor (suhu + checksum, kelembaban + checksum)
            result = bytearray(6)
            self.i2c_device.readfrom_into(self.address, result)

            # Memisahkan data suhu dan kelembaban beserta CRC-nya
            temperature_raw = result[0] << 8 | result[1]
            temperature_crc = result[2]
            humidity_raw = result[3] << 8 | result[4]
            humidity_crc = result[5]

            # Validasi checksum untuk suhu
            if self.crc8(result[:2]) != temperature_crc:
                print("CRC error pada suhu")
                return None, None

            # Validasi checksum untuk kelembaban
            if self.crc8(result[3:5]) != humidity_crc:
                print("CRC error pada kelembaban")
                return None, None

            # Konversi nilai suhu dan kelembaban dari data mentah
            temperature = -45 + (175 * temperature_raw / 65535.0)
            humidity = 100 * humidity_raw / 65535.0

            return temperature, humidity  # Mengembalikan nilai suhu dan kelembaban

        except Exception as e:
            print(f"Error reading SHT31 sensor: {e}")
            return None, None

    def get_temperature_humidity(self):
        """
        Fungsi untuk terus-menerus membaca data suhu dan kelembaban dari sensor hingga mendapatkan nilai yang valid.
        """
        while True:
            temperature, humidity = self.read_data()
            if temperature is not None and humidity is not None:
                return temperature, humidity  # Mengembalikan nilai suhu dan kelembaban yang valid
            time.sleep(0.1)  # Delay untuk stabilisasi jika tidak ada data
