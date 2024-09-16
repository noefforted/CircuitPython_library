import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

class PCF8574T:
    def __init__(self, i2c, address=0x20):
        """Inisialisasi PCF8574 dengan I2C."""
        self.i2c_device = I2CDevice(i2c, address)
        self.gpio_state = 0xFF  # Semua pin awalnya HIGH (input)

    def write_pin(self, pin, value):
        """Menulis nilai ke pin tertentu pada PCF8574 (0-7)."""
        if value:
            self.gpio_state |= (1 << pin)  # Set bit ke 1 (HIGH)
        else:
            self.gpio_state &= ~(1 << pin)  # Set bit ke 0 (LOW)
        self._write_output()

    def read_pin(self, pin):
        """Membaca status pin tertentu pada PCF8574 (0-7)."""
        self._read_input()
        return bool(self.gpio_state & (1 << pin))

    def _write_output(self):
        """Menulis seluruh byte state ke PCF8574."""
        with self.i2c_device as i2c:
            i2c.write(bytes([self.gpio_state]))

    def _read_input(self):
        """Membaca state dari PCF8574."""
        with self.i2c_device as i2c:
            result = bytearray(1)
            i2c.readinto(result)
        self.gpio_state = result[0]

# Contoh penggunaan
i2c = busio.I2C(board.SCL, board.SDA)
expander = PCF8574T(i2c)

# Contoh: Set pin 0 menjadi LOW
expander.write_pin(0, False)

# Contoh: Membaca status pin 0
pin_status = expander.read_pin(0)
print(f"Pin 0 is {'HIGH' if pin_status else 'LOW'}")
