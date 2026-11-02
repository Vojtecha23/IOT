from machine import Pin, UART
from time import sleep_ms
button = Pin(16, Pin.IN, Pin.PULL_UP)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
prev = None
while True:
    pressed = button.value() == 0
    if pressed != prev:
        sleep_ms(25)
        if (button.value() == 0) == pressed:
            prev = pressed
            message = 'ZAPNI\n' if pressed else 'VYPNI\n'
            uart.write(message)
            print('Odeslano:', message.strip())
    sleep_ms(10)
