import RPi.GPIO as GPIO
import time
import network_scanner
import sys
from threading import Thread

from healthbar import HealthBar
from read import Reader
from display import Display
from button import Button

# address = sys.argv[1]

NFC_MSG = None
        
def NFC_reading():
    reader = Reader()
    while True:
        id,text = reader.read()
        print(id, text)
        NFC_MSG = text

class DosimeterMock:
    def __init__(self):
        #GPIO Basic initialization
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

        status_led_pin = 21
        GPIO.setup(status_led_pin,GPIO.OUT)
        self.HP = 100

        leds = [5,6,13,19,26,20]
        self.HPBar = HealthBar(leds, maxval=self.HP)

        self.display = Display(clk_pin=3, dio_pin=2)

        self.button = Button(4)

    def check_NFC(self):
        msg = NFC_MSG
        NFC_MSG = None
        if msg is None:
            return
        if msg == "HP":
            self.HP = 100


    def loop(self):
        NFC_thread = Thread(target=NFC_reading, args=[])
        NFC_thread.start()
        while True:
            try:
                # strength = -network_scanner.get_signal_strength(address)
                print("cycle")
                self.HPBar.display(HP)
                self.check_NFC()
                self.display.display_time()
                HP -= 1
            except Exception as e:
                print('Excetion', str(e))
            time.sleep(0.1)


if __name__ == "__main__":
    dm = DosimeterMock()
    dm.loop()
