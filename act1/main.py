from machine import Pin, ADC
from time import sleep
import bluetooth
import neopixel
from ble_advertising import advertising_payload
from ble_uart_peripheral import *

ble = bluetooth.BLE()
uart = BLEUART(ble, "esp1")

isActivated = 0

def on_rx():
    res = uart.read().decode().strip()
    print(res)
    if res == "ok":
        global isActivated
        isActivated = 1
        print(isActivated)

uart.irq(handler=on_rx)

#Anemometer
# Resistor Divider at ADC input
R_BRIDGE_RATIO = 0.68117
pinAnemo = Pin(34, Pin.IN)
ana = ADC(pinAnemo)
#ana2 = ADC(Pin(14))
ana.atten( ADC.ATTN_11DB ) # Full 3.3V Range

#led
n = 400
p = 5
maxLight = 400
r = 255
g = 0
b = 0

while True:
    if isActivated == 0:
        value = ana.read_uv() # 0..4095
        value = value/1000
        #value2 = ana2.read()
        v_esp = 3.3 * value / 4096
        v_anem = v_esp / R_BRIDGE_RATIO
        # Vitesse vent m/h
        speed_mps = 6 * v_anem
        # Vitesse vent en km/h
        speed_kmph = speed_mps * 3.6

        print( "value 27: ", value )
        print("pin : ", pinAnemo.value())
        print( "m/s:", speed_mps )
        print( "km/h:", speed_kmph )
        print( "--------------------" )
        if speed_kmph > 5:
          uart.write("esp1On")
        sleep( 0.2 )
    else:
        np = neopixel.NeoPixel(Pin(p),n)
        for i in range(maxLight):
          np[i] = (r, g, b)
          np.write()
          sleep(0.05)
    

uart.close()

