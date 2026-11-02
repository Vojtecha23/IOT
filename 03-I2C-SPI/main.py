from machine import Pin, I2C, time_pulse_us
from time import sleep_us, sleep_ms
from pico_i2c_lcd import I2cLcd

trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
found = i2c.scan()
if not found:
    raise RuntimeError('LCD nenalezeno: zkontroluj I2C a napajeni')
addr = 0x27 if 0x27 in found else 0x3F if 0x3F in found else found[0]
lcd = I2cLcd(i2c, addr, 2, 16)

def measure_cm():
    trig.off()
    sleep_us(3)
    trig.on()
    sleep_us(10)
    trig.off()
    pulse = time_pulse_us(echo, 1, 30000)
    if pulse < 0:
        return None
    return pulse * 0.0343 / 2

try:
    while True:
        d = measure_cm()
        lcd.move_to(0, 0)
        lcd.putstr('Vzdalenost:     ')
        lcd.move_to(0, 1)
        lcd.putstr((('%.1f cm' % d) if d is not None else 'Bez odezvy').ljust(16))
        print('Vzdalenost:', d)
        sleep_ms(300)
finally:
    lcd.clear()
