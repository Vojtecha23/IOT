from machine import UART, Pin
import time
 
# UART musí mít stejné parametry jako odesílatel
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
 
# LED dioda na pinu GP15
led = Pin(15, Pin.OUT)
 
print("Čekám na povely od tlačítka...")
 
while True:
    # Pokud jsou na sběrnici nová data
    if uart.any() > 0:
        # Přečtení povelu a odstranění neviditelných znaků (\n)
        povel = uart.readline().decode('utf-8').strip()
        print("Přijato:", povel)
        # Vyhodnocení povelu
        if povel == "ZAPNI":
            led.value(1)
        elif povel == "VYPNI":
            led.value(0)
    time.sleep(0.05)