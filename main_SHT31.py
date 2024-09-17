import time
from SHT31 import SHT31

def main():
    sensor = SHT31(i2c_address=0x44)
    while True:
        temperature, humidity = sensor.get_temperature_humidity()
        if temperature is not None and humidity is not None:
            print(f"Suhu = {temperature:.2f}°C, Kelembaban = {humidity:.2f}%")
        time.sleep(1) 

if __name__ == "__main__":
    main()
