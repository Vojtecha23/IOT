import tkinter as tk
from gpiozero import MCP3008, PWMOutputDevice

adc = MCP3008(channel=0)
# pasivni piezo bzucak, PWM; u aktivniho nemusí menit hlasitost
buzzer = PWMOutputDevice(18, frequency=1000, initial_value=0)
root = tk.Tk()
root.title('Analogovy vstup + PWM')
root.geometry('390x240')
label = tk.Label(root, font=('Arial', 15))
label.pack(pady=10)
scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Softwarovy limit (%)', length=300)
scale.set(100)
scale.pack()

def update():
    physical = adc.value
    duty = physical * scale.get() / 100
    buzzer.value = duty
    label.config(text='Potenciometr: %d %% | PWM: %d %%' % (physical*100, duty*100))
    root.after(100, update)

def close():
    buzzer.off()
    buzzer.close()
    adc.close()
    root.destroy()
root.protocol('WM_DELETE_WINDOW', close)
update()
root.mainloop()
