import machine, neopixel, time
import bluetooth
from ble_advertising import advertising_payload
from ble_uart_peripheral import *

ble = bluetooth.BLE()
uart = BLEUART(ble, "esp1")

# define neopixel
pin = 5
n = 300
np = neopixel.NeoPixel(machine.Pin(pin), n)

# to folow the current led 
currentLed = 0

rr = 40
gr = 15
br = 0

rh = 60
gh = 80
bh = 40

# waiting, running, end
status = "waiting"
endIsSend = 0

def init():
    global status
    status = "waiting"
    for i in range(n):
        np[i] = (0, 0, 0)
        np.write()
        
def on_rx():
    global status
    status = uart.read().decode().strip()
    print(status)
    uart.write(status)
    if status == "reset":
        init()
        
def glowLight(r, g, b, i):
    
    currentLed = i
    minLed = currentLed - 10
           
    if n > i:
        np[i] = (r, g, b)
            
    if minLed > -1:             
        np[minLed] = (int(r/2), int(g/2), int(b/2))

        
def stepGlowLights(r, g, b, start, delai):
    
    if(start == 1) :
        for i in range(0, int(n/2) + 10):
            glowLight(r, g, b, i)
            time.sleep(delai)
            np.write()
    
    else :
        for i in range(int(n/2), n + 10):
            glowLight(r, g, b, i)
            time.sleep(delai)
            np.write()

def  currentCode() :
    print("running")
    # code ...

######### code for led
            
# reset led
init()

uart.irq(handler=on_rx)

while True:
        
    if status == "running" :
        stepGlowLights(rr, gr, br, 0, 0)
        # envoie d'un message à un autre appareil que le ble symbiose : exemple alumé l'écran des mycorise
        # uart2.write("draw abithing")

    elif status == "currentStep" :
        # fonction qui contiendra le code
        currentCode()
    
    elif status == "end" :
        if(endIsSend == 1) :
            # voir pour changer le message en fonction de la fin de l'expérience
            uart.write("next step")
            endIsSend = 1
            
        stepGlowLights(rh, gh, bh, 1, 0)
        
uart.close()

