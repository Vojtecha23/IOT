import machine
import time
from machine import I2C, Pin

# Import knihovny pro displej (název modulu se může mírně lišit podle staženého balíčku)

from pico_i2c_lcd import I2cLcd

# Nastavení pinů pro HC-SR04
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

# Inicializace I2C (SDA = GP4, SCL = GP5, frekvence 400kHz)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Zjištění adresy displeje na sběrnici
devices = i2c.scan()

if len(devices) == 0:
    print("Chyba: I2C displej nebyl nalezen. Zkontroluj zapojení SDA a SCL.")
else:
    # Vytvoření objektu displeje (adresa, počet řádků, počet znaků na řádek)
    lcd = I2cLcd(i2c, devices[0], 2, 16)
    
    lcd.putstr("Pico W start...")
    time.sleep(1.5)
    lcd.clear()

    while True:
        # Generování 10us pulzu na Trig pinu
        trig.low()
        time.sleep_us(2)
        trig.high()
        time.sleep_us(10)
        trig.low()
        
        # Čekání na začátek a konec odrazu
        while echo.value() == 0:
            start_t = time.ticks_us()
        while echo.value() == 1:
            end_t = time.ticks_us()
            
        # Výpočet trvání a převod na vzdálenost
        duration = time.ticks_diff(end_t, start_t)
        distance = (duration * 0.0343) / 2
        
        # Výpis do konzole v Thonny (pro debugování)
        print("Vzdálenost: {:.1f} cm".format(distance))
        
        # Zobrazení na LCD displeji
        lcd.move_to(0, 0)
        lcd.putstr("Vzdalenost:     ")
        lcd.move_to(0, 1)
        # Přidání mezer na konec maže zbytky předchozích delších čísel
        lcd.putstr(str(int(distance)) + " cm       ")
        
        time.sleep(0.25)