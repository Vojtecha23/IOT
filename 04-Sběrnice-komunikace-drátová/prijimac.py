from machine import Pin, UART
from time import sleep_ms
led = Pin(15, Pin.OUT)
led.off()
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
buffer = b''
while True:
    if uart.any():
        buffer += uart.read()
        if len(buffer) > 100:
            buffer = b''
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            cmd = line.strip()
            if cmd == b'ZAPNI':
                led.on()
            elif cmd == b'VYPNI':
                led.off()
            print('Povel:', cmd)
    sleep_ms(10)
