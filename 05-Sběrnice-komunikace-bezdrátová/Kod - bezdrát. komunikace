import network
import socket
from machine import Pin
import time
 
network.country('CZ')
led = Pin(15, Pin.OUT)
 
ap = network.WLAN(network.AP_IF)
# Nastavíme security=0, což znamená otevřenou síť bez hesla
ap.config(ssid='PicoSit', security=0)
ap.active(True)
 
print("Vytvářím otevřenou Wi-Fi síť 'PicoSit'...")
# Dáme mu 3 vteřiny natvrdo, ať se rádio stihne probrat
time.sleep(3)
 
ip_adresa = ap.ifconfig()[0]
print("Wi-Fi běží! Moje IP adresa je:", ip_adresa)
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 5000))
s.setblocking(False)
 
print("Čekám na povely...")
 
while True:
    try:
        data, addr = s.recvfrom(1024)
        povel = data.decode('utf-8').strip()
        print("Přijato od", addr[0], ":", povel)
        if povel == "ZAPNI":
            led.value(1)
        elif povel == "VYPNI":
            led.value(0)
    except OSError:
        pass
    time.sleep(0.05),