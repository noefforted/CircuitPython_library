import serial
import time

class A02YYUW:
    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=1):
        """
        Inisialisasi sensor A02YYUW dengan PySerial.
        """
        self.uart = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.data = [0] * 4  # Buffer untuk menyimpan 4 byte data

    def rotate_data(self):
        """
        Fungsi untuk merotasi array sehingga byte 0xFF (255) selalu berada di posisi pertama (data[0]).
        """
        for i in range(4):
            if self.data[i] == 0xFF:
                # Rotasi array sehingga 0xFF berada di posisi data[0]
                while i != 0:
                    temp = self.data[0]
                    for j in range(3):
                        self.data[j] = self.data[j + 1]
                    self.data[3] = temp
                    i -= 1
                break

    def read_data(self):
        """
        Membaca data dari sensor dan memvalidasi checksum serta menghitung jarak.
        """
        if self.uart.in_waiting >= 4:
            # Membaca 4 byte dari UART
            self.data = [ord(self.uart.read(1)) for _ in range(4)]

            # Rotasi data jika 0xFF tidak berada di posisi pertama
            self.rotate_data()

            header = self.data[0]
            msb = self.data[1]
            lsb = self.data[2]
            crc = self.data[3]

            # Pastikan header adalah 0xFF
            if header == 0xFF:
                # Hitung checksum
                checksum = (0xFF + msb + lsb) & 0xFF

                # Jika checksum valid, hitung jarak
                if checksum == crc:
                    distance = (msb << 8) | lsb
                    return distance
                else:
                    return None
            else:
                return None
        else:
            return None

    def get_distance(self):
        """
        Fungsi untuk terus-menerus membaca jarak dari sensor hingga mendapatkan data valid.
        """
        while True:
            distance = self.read_data()
            if distance is not None:
                return distance  # Mengembalikan jarak yang valid
            time.sleep(0.1)  # Delay untuk stabilisasi jika tidak ada data