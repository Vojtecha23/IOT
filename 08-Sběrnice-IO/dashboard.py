import tkinter as tk
from gpiozero import MCP3008
import smbus2
import time

ADDR = 0x27
bus = smbus2.SMBus(1)
adc = MCP3008(channel=0)
root = tk.Tk()
root.title('I2C LCD + ADC dashboard')
root.geometry('390x190')
label = tk.Label(root, font=('Arial', 17))
label.pack(pady=15)
bar = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Softwarovy offset (-50 az +50)', length=300)
bar.set(50)
bar.pack()

def write4(nib, mode):
    data = (nib & 0xF0) | mode | 0x08
    bus.write_byte(ADDR, data)
    bus.write_byte(ADDR, data | 0x04)
    time.sleep(0.0001)
    bus.write_byte(ADDR, data)

def send(value, mode=0):
    write4(value & 0xF0, mode)
    write4((value << 4) & 0xF0, mode)

def init():
    time.sleep(0.05)
    for value in (0x30,0x30,0x30,0x20):
        write4(value, 0)
        time.sleep(0.005)
    for cmd in (0x28, 0x08, 0x01, 0x06, 0x0C):
        send(cmd)
        time.sleep(0.003)

def display(row, line):
    send(0x80 if row == 0 else 0xC0)
    for ch in line.ljust(16)[:16]:
        send(ord(ch), 1)

init()

def update():
    raw = round(adc.value*100)
    result = min(100, max(0, raw + bar.get() - 50))
    label.config(text='Fyzicky vstup: %d %% | LCD: %d %%' % (raw, result))
    try:
        display(0, 'Potenciometr ADC')
        display(1, 'Hodnota: %3d %%' % result)
    except OSError as e:
        label.config(text='I2C chyba: %s' % e)
    root.after(200, update)

def close():
    try:
        send(0x01)
    finally:
        adc.close()
        bus.close()
        root.destroy()
root.protocol('WM_DELETE_WINDOW', close)
update()
root.mainloop()
