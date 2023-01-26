import RPi.GPIO as GPIO
import time
import network_scanner
import sys
from threading import Thread
from enum import Enum

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

class State(Enum):
    RADIATION = 1
    TIME = 2
    HEALTH = 3
    GOAL_DISTANCE = 4
    FINISHED = 10

next_state = {
    State.FINISHED: State.FINISHED,
    State.RADIATION : State.TIME,
    State.TIME : State.HEALTH,
    State.HEALTH : State.GOAL_DISTANCE,
    State.GOAL_DISTANCE : State.RADIATION,
}

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
        self.button_hold_last_time = False

        self.state = State.GOAL_DISTANCE
        self.radiation_strength = 0
        self.goal_distance = 100

    def check_NFC(self):
        msg = NFC_MSG
        NFC_MSG = None
        if msg is None:
            return
        if msg == "HP":
            self.HP = 100

    def handle_state(self):
        button_hold = self.button.is_hold()
        if button_hold and not self.button_hold_last_time:
            self.state = next_state(self.state)
        self.button_hold_last_time = button_hold

        if self.state == State.TIME:
            self.display.display_time()
        elif self.state == State.HEALTH:
            self.display.display_number('H', self.HP)
        elif self.state == State.RADIATION:
            self.display.display_number('R', self.radiation_strength)
        elif self.state == State.GOAL_DISTANCE:
            self.display.display_number('G', self.goal_distance)
        raise Exception("Unknown state " + str(self.state))

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
