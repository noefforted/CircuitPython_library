import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

class MCP3008:
    def __init__(self, spi, cs):
        """Inisialisasi MCP3008 dengan SPI."""
        self.cs = digitalio.DigitalInOut(cs)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        self.spi_device = SPIDevice(spi, self.cs)

    def read_channel(self, channel):
        """Membaca nilai dari channel tertentu (0-7) pada MCP3008."""
        if channel < 0 or channel > 7:
            raise ValueError("Channel harus antara 0 dan 7.")

        # Kirim perintah 3-byte ke MCP3008:
        # Start bit (1), Single/Diff (1), D2-D0 (channel select bits), dan 10 bit data
        command = 0x18 | (channel << 4)  # Start bit + channel number
        buffer = bytearray([command, 0x00, 0x00])
        
        with self.spi_device as spi:
            spi.write(buffer)
            spi.readinto(buffer)

        # Ambil 10-bit ADC dari 2 byte terakhir
        result = ((buffer[1] & 0x03) << 8) | buffer[2]
        return result

# Contoh penggunaan
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = board.D5  # Pin chip select (CS)
adc = MCP3008(spi, cs)

# Baca channel 0
value = adc.read_channel(0)
print(f"Nilai ADC dari channel 0: {value}")
