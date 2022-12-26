from machine import Pin, ADC
from time import sleep

# Resistor Divider at ADC input
R_BRIDGE_RATIO = 0.68117

ana = ADC(Pin(27))
ana.atten( ADC.ATTN_11DB ) # Full 3.3V Range

while True:
   value = ana.read() # 0..4095
   v_esp = 3.3 * value / 4096
   v_anem = v_esp / R_BRIDGE_RATIO
   # Vitesse vent m/h
   speed_mps = 6 * v_anem
   # Vitesse vent en km/h
   speed_kmph = speed_mps * 3.6

   print( "value: ", value )
   print( "m/s:", speed_mps )
   print( "km/h:", speed_kmph )
   print( "--------------------" )
   sleep( 0.5 )