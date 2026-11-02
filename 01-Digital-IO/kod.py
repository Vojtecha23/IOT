from machine import Pin
from time import sleep_ms

# Tlačítko GP14 -> GND; LED GP15 -> odpor -> GND.
# Shodně s původním popisem: po stisknutí LED zhasne.
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)
led = Pin(15, Pin.OUT)

while True:
    led.value(tlacitko.value())
    sleep_ms(30)
