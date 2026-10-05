from machine import Pin, ADC, PWM
import time

# Nastavení analogového vstupu (ADC) na pinu GP26
potenciometr = ADC(Pin(26))

# Nastavení PWM výstupu na pinu GP15 pro naši LED
led_pwm = PWM(Pin(15))
led_pwm.freq(1000) # Nastavení frekvence PWM blikání na 1000 Hz (neviditelné pro oko)

print("Otáčejte potenciometrem pro změnu jasu LED.")

while True:
    # Přečtení analogové hodnoty (vrací číslo od 0 do 65535)
    hodnota_adc = potenciometr.read_u16()
    
    # Nastavení jasu LED (bere číslo od 0 do 65535)
    led_pwm.duty_u16(hodnota_adc)
    
    # Volitelně: výpis hodnoty do konzole pro kontrolu
    # print("Hodnota:", hodnota_adc)
    
    # Velmi krátká pauza pro plynulý chod
    time.sleep(0.01)