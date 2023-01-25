import RPi.GPIO as GPIO
import time
import network_scanner
import sys
from threading import Thread

from healthbar import HealthBar
from read import Reader
from display import Display

# address = sys.argv[1]

#GPIO Basic initialization
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

status_led_pin = 21
GPIO.setup(status_led_pin,GPIO.OUT)
HP = 100

leds = [5,6,13,19,26,20]
HPBar = HealthBar(leds, maxval=HP)

display = Display(clk_pin=3, dio_pin=2)

NFC_MSG = None

def check_NFC():
    msg = NFC_MSG
    NFC_MSG = None
    if msg is None:
        return
    if msg == "HP":
        HP = 100

def NFC_reading():
    reader = Reader()
    while True:
        id,text = reader.read()
        print(id, text)
        NFC_MSG = text

NFC_thread = Thread(target=NFC_reading, args=[])
while True:
    try:
        # strength = -network_scanner.get_signal_strength(address)
        print("cycle")
        HPBar.display(HP)
        check_NFC()
        display.display_time()
        HP -= 1
    except Exception as e:
        print('Excetion', str(e))
    time.sleep(0.1)


