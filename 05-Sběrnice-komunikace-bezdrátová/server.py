import network, socket, time
from machine import Pin
led = Pin(15, Pin.OUT)
led.off()
ap = network.WLAN(network.AP_IF)
ap.config(essid='PicoSit', password='PicoDemo123')
ap.active(True)
for _ in range(50):
    if ap.active():
        break
    time.sleep_ms(100)
print('IP:', ap.ifconfig()[0])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5000))
s.settimeout(0.3)
try:
    while True:
        try:
            data, addr = s.recvfrom(128)
        except OSError:
            continue
        cmd = data.strip()
        if cmd == b'ZAPNI': led.on()
        elif cmd == b'VYPNI': led.off()
        print(addr, cmd)
finally:
    s.close()
    ap.active(False)
