import time
from A02YYUW import A02YYUW 

def main():
    sensor = A02YYUW(port="/dev/serial0", baudrate=9600)
    while True:
        distance = sensor.get_distance()
        print(f"Jarak = {distance/10:.2f} cm")
        time.sleep(0.1)  

# if __name__ == "__main__":
main()
