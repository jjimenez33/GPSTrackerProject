from machine import Pin, I2C, UART
import time

GPS = UART(1,
           baudrate = 9600,
           tx=machine.Pin(8),
           rx=machine.Pin(9)
)

try:
    while True:
        if GPS.any():
            myChar = GPS.read(1).decode('utf-8')
            print(myChar, end="")


except KeyboardInterrupt:
    print("\n Program Interrupted!")

finally:
    print("\n . . . Cleaning up UART")
    GPS.deinit()
    print("Cleanly Exited UART")
