import serial
import time

class A02YYUW:
    def __init__(self, port="/dev/ttyS0", baudrate=9600):
        """Inisialisasi komunikasi serial dengan sensor A02YYUW"""
        self.ser = serial.Serial(port, baudrate)
        self.ser.flush()

    def read_distance(self):
        """Membaca data jarak dari sensor A02YYUW"""
        try:
            if self.ser.in_waiting > 0:
                data = self.ser.read(4)  # Membaca 4 byte data dari sensor
                if len(data) == 4:
                    distance = (data[1] << 8) | data[2]  # Menggabungkan byte ke-2 dan ke-3 menjadi nilai jarak
                    if data[0] == 0xFF and data[3] == sum(data[:3]) & 0xFF:
                        return distance / 10.0  # Konversi ke cm
        except Exception as e:
            print(f"Error: {e}")
        return None

    def close(self):
        """Menutup koneksi serial"""
        self.ser.close()
