"""Uloha 08: physical MCP3008 input, I2C LCD, optional TM1637 and Tkinter."""
import tkinter as tk
import time
from gpiozero import MCP3008
from smbus2 import SMBus

# 7segment modul vyzaduje knihovnu tm1637; pokud neni pripojen, ponechte False.
POUZIT_TM1637 = True
LCD_ADRESA = 0x27  # pripadne 0x3F podle i2cdetect -y 1

adc = MCP3008(channel=0)
bus = SMBus(1)
segment = None
if POUZIT_TM1637:
    import tm1637
    segment = tm1637.TM1637(clk=21, dio=20)
    segment.brightness(2)


def nibble(cast, rs=0):
    bits = (cast & 0xF0) | rs | 0x08
    bus.write_byte(LCD_ADRESA, bits)
    bus.write_byte(LCD_ADRESA, bits | 0x04)
    time.sleep(0.0001)
    bus.write_byte(LCD_ADRESA, bits)


def lcd_send(byte, rs=0):
    nibble(byte & 0xF0, rs)
    nibble((byte << 4) & 0xF0, rs)


def lcd_init():
    time.sleep(0.05)
    for cmd in (0x30, 0x30, 0x30, 0x20):
        nibble(cmd)
        time.sleep(0.005)
    for cmd in (0x28, 0x08, 0x01, 0x06, 0x0C):
        lcd_send(cmd)
        time.sleep(0.005)


def lcd_row(index, message):
    lcd_send(0x80 if index == 0 else 0xC0)
    for char in message.ljust(16)[:16]:
        lcd_send(ord(char), 1)


lcd_init()
okno = tk.Tk()
okno.title('08 - Fyzicky vstup + LCD I2C')
okno.geometry('460x245')
text = tk.StringVar(value='Cekam na hodnotu...')
tk.Label(okno, text='Potenciometr + LCD + 7segment', font=('Arial', 14, 'bold')).pack(pady=12)
tk.Label(okno, textvariable=text, font=('Arial', 12)).pack()
tk.Label(okno, text='Softwarova korekce: -50 az +50').pack(pady=(12, 0))
korekce = tk.Scale(okno, from_=-50, to=50, orient=tk.HORIZONTAL, length=320)
korekce.set(0)
korekce.pack()
posledni = None

def obnov():
    global posledni
    try:
        fyzicka = round(adc.value * 100)
        vysledek = max(0, min(100, fyzicka + korekce.get()))
        text.set(f'Potenciometr {fyzicka} %  |  LCD {vysledek} %')
        if vysledek != posledni:
            lcd_row(0, 'Hodnota ADC:')
            lcd_row(1, f'-- > {vysledek:3d} %')
            if segment:
                segment.number(vysledek)
            posledni = vysledek
    except OSError as exc:
        text.set(f'Chyba I2C: {exc}')
    except Exception as exc:
        text.set(f'Chyba: {exc}')
    okno.after(200, obnov)

def zavrit():
    try:
        lcd_send(0x01)
        if segment:
            segment.write([0, 0, 0, 0])
    finally:
        bus.close()
        adc.close()
        okno.destroy()

okno.protocol('WM_DELETE_WINDOW', zavrit)
obnov()
okno.mainloop()
