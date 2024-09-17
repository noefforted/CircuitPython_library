import serial
import time

# Inisialisasi UART dengan PySerial
uart = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=1)

def read_data():
    """
    Membaca dan mencetak semua data dari sensor termasuk header dan jarak
    """
    while True:
        if uart.in_waiting >= 4:  # Pastikan ada setidaknya 4 byte data yang tersedia
            # Menunggu sampai byte pertama (header) adalah 0xFF (255)
            header = ord(uart.read(1))
            if header == 0xFF:
                # Membaca byte lainnya
                dataPayloadMsb = ord(uart.read(1))  # Byte kedua (MSB)
                dataPayloadLsb = ord(uart.read(1))  # Byte ketiga (LSB)
                dataCrc = ord(uart.read(1))         # Byte keempat (Checksum)

                # Hitung checksum
                checkSum = (0xFF + dataPayloadMsb + dataPayloadLsb) & 0xFF

                # Menggabungkan MSB dan LSB menjadi satu nilai 16-bit untuk jarak
                result = (dataPayloadMsb << 8) | dataPayloadLsb

                # Cetak semua data
                print(f"Header: {header}")
                print(f"MSB: {dataPayloadMsb}")
                print(f"LSB: {dataPayloadLsb}")
                print(f"CRC: {dataCrc}")

                # Validasi checksum dan cetak jarak jika valid
                if checkSum == dataCrc:
                    print(f"Jarak: {result} cm")
                else:
                    print("Checksum tidak valid")

                print("-" * 30)  # Pembatas antar pembacaan

if __name__ == "__main__":
    read_data()
    time.sleep(0.1)
