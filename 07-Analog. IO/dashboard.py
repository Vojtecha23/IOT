"""Uloha 07: MCP3008 analog input + PWM buzzer + servo + Tkinter."""
import tkinter as tk
from gpiozero import MCP3008, PWMOutputDevice, Servo

POT_KANAL = 0
GPIO_BZUCAK = 18
GPIO_SERVO = 13

adc = MCP3008(channel=POT_KANAL)
bzucak = PWMOutputDevice(GPIO_BZUCAK, frequency=1000, initial_value=0)
servo = Servo(GPIO_SERVO, initial_value=0)

okno = tk.Tk()
okno.title('07 - Analogovy vstup a PWM dashboard')
okno.geometry('470x340')

stav = tk.StringVar(value='Nacitam analogovy vstup...')
tk.Label(okno, text='Fyzicky potenciometr + PWM bzucak', font=('Arial', 13, 'bold')).pack(pady=(12, 3))
tk.Label(okno, textvariable=stav, font=('Arial', 12)).pack(pady=5)

tk.Label(okno, text='Posuvnik urcuje maximalni PWM (%)').pack()
limit = tk.Scale(okno, from_=0, to=100, orient=tk.HORIZONTAL, length=320)
limit.set(100)
limit.pack()

tk.Label(okno, text='Natoceni serva (0 az 180 stupnu)').pack(pady=(10, 0))
uhel = tk.Scale(okno, from_=0, to=180, orient=tk.HORIZONTAL, length=320)
uhel.set(90)
uhel.pack()

def obnov():
    try:
        analog = adc.value
        duty = analog * limit.get() / 100.0
        bzucak.value = duty
        servo.value = (uhel.get() / 90.0) - 1.0
        stav.set(f'Potenciometr: {analog * 100:.0f} %  |  PWM: {duty * 100:.0f} %  |  Servo: {uhel.get()}°')
    except Exception as exc:
        stav.set(f'Chyba vstupu/vystupu: {exc}')
    okno.after(150, obnov)

def zavrit():
    bzucak.off()
    bzucak.close()
    servo.detach()
    servo.close()
    adc.close()
    okno.destroy()

okno.protocol('WM_DELETE_WINDOW', zavrit)
obnov()
okno.mainloop()
