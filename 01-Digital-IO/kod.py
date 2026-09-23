from machine import Pin
import time

# --- Nastavení ---
# LED připojená na GP15 jako výstup
led = Pin(15, Pin.OUT) 

# Tlačítko připojené na GP14 jako vstup s interním PULL-UP rezistorem
tlacitko = Pin(14, Pin.IN, Pin.PULL_UP)

print("Program spuštěn. Zmáčkni tlačítko.")

# --- Hlavní smyčka ---
while True:
    # Zde je to prohozené: reagujeme na hodnotu 1
    if tlacitko.value() == 1:
        led.value(1)     # Rozsviť LED
    else:
        led.value(0)     # Zhasni LED
        
    time.sleep(0.1)      # Krátká pauza (základní debouncing)