import tkinter as tk
from gpiozero import LED, Button
led = LED(17)
button = Button(27, pull_up=True, bounce_time=0.05)
root = tk.Tk()
root.title('Digital IO dashboard')
root.geometry('350x180')
widget = tk.Button(root, font=('Arial', 22), command=lambda: led.toggle())
widget.pack(expand=True, fill='both', padx=15, pady=15)
# GPIO callback nikdy neupravuje Tkinter; GUI samo cte stav ve svem vlakne.
button.when_pressed = led.toggle

def refresh():
    state = led.is_lit
    widget.config(text='ZAPNUTO' if state else 'VYPNUTO', bg='green' if state else 'red')
    root.after(80, refresh)

def close():
    led.off()
    button.close()
    led.close()
    root.destroy()
root.protocol('WM_DELETE_WINDOW', close)
refresh()
root.mainloop()
