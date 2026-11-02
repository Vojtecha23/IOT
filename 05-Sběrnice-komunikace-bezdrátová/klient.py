import network, socket, time
from machine import Pin
button = Pin(16, Pin.IN, Pin.PULL_UP)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('PicoSit', 'PicoDemo123')
for _ in range(150):
    if wlan.isconnected(): break
    time.sleep_ms(100)
if not wlan.isconnected():
    raise RuntimeError('Klient se nepripojil k PicoSit')
server_ip = '192.168.4.1'  # oveř IP v konzoli serveru
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
previous = None
try:
    while True:
        pressed = button.value() == 0
        if pressed != previous:
            time.sleep_ms(25)
            if (button.value() == 0) == pressed:
                previous = pressed
                cmd = b'ZAPNI' if pressed else b'VYPNI'
                for _ in range(3):
                    s.sendto(cmd, (server_ip, 5000))
                    time.sleep_ms(30)
                print(cmd)
        time.sleep_ms(10)
finally:
    s.close()
    wlan.active(False)
