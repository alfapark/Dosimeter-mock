import RPi.GPIO as GPIO
import time
import network_scanner
import sys
from threading import Thread
from enum import Enum
import traceback
import json

from healthbar import HealthBar
from read import Reader
from display import Display
from button import Button

# address = sys.argv[1]

def load_json_file(file_location):
    data = dict()
    try:
        with open(file_location) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        pass
    return data

NFC_MSG = None        

def NFC_reading():
    global NFC_MSG
    reader = Reader()
    while True:
        id,text = reader.read()
        print(id, text)
        NFC_MSG = text
        time.sleep(1)

WIFI_signals = dict()

def WIFI_reading():
    global WIFI_signals
    while True:
        WIFI_signals = network_scanner.parse_signal_strengths()
        time.sleep(1)

class State(Enum):
    RADIATION = 1
    TIME = 2
    HEALTH = 3
    GOAL_DISTANCE = 4
    FINISHED = 10
    DEAD = 11

next_state = {
    State.FINISHED: State.FINISHED,
    State.DEAD: State.DEAD,
    State.RADIATION : State.TIME,
    State.TIME : State.HEALTH,
    State.HEALTH : State.GOAL_DISTANCE,
    State.GOAL_DISTANCE : State.RADIATION,
}

class DosimeterMock:
    def __init__(self):
        self.set_initial_state()
        #GPIO Basic initialization
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

        status_led_pin = 21
        GPIO.setup(status_led_pin,GPIO.OUT)

        leds = [20,26,19,13,6,5]
        self.HPBar = HealthBar(leds, maxval=self.HP)

        self.display = Display(clk_pin=3, dio_pin=2)

        self.button = Button(4)
        self.button_hold_last_time = False

        self.parse_config()

    def parse_config(self):
        config_dict = load_json_file("config.json")
        self.goal_address = config_dict["goal_adr"]
        self.radiation_addresses = config_dict["radiation_adrs"]


    def set_initial_state(self):
        self.state = State.GOAL_DISTANCE
        self.radiation_strength = 0
        self.goal_distance = 100
        self.HP = 100
        self.start = time.time()

    def get_elapsed_seconds(self):
        elapsed = time.time() - self.start
        return int(elapsed)

    def check_NFC(self):
        global NFC_MSG
        msg = NFC_MSG
        NFC_MSG = None
        if msg is None:
            return
        msg = msg.strip()
        print(msg)
        if msg == "HP":
            self.HP = 100
        elif msg == "GOAL":
            self.state = State.FINISHED
        elif msg == "RESET":
            self.set_initial_state()

    def handle_state(self):
        button_hold = self.button.is_hold()
        if button_hold and not self.button_hold_last_time:
            self.state = next_state[self.state]
        self.button_hold_last_time = button_hold

        if self.state == State.TIME:
            self.display.display_time(self.get_elapsed_seconds())
        elif self.state == State.HEALTH:
            self.display.display_number('H', self.HP)
        elif self.state == State.RADIATION:
            self.display.display_number('R', self.radiation_strength)
        elif self.state == State.GOAL_DISTANCE:
            self.display.display_number('G', self.goal_distance)
        elif self.state not in [State.FINISHED, State.DEAD]:
            raise Exception("Wrong state: " + str(self.state))

    def check_game(self):
        if self.HP <= 0:
            self.state = State.DEAD
            self.display.display_text("dead")
        if self.state == State.FINISHED:
            self.display.display_time(self.get_elapsed_seconds())

    def game_ended(self):
        return self.state in [State.DEAD, State.FINISHED]

    def handle_network(self):
        global WIFI_signals
        signals = WIFI_signals
        self.goal_distance = 999
        if self.goal_address in signals:
            self.goal_distance = -signals[self.goal_address]
        self.radiation_strength = 0
        for address in self.radiation_addresses:
            if address in signals:
                self.radiation_strength += signals[self.goal_address] + 100

    def update_HP(self):
        self.HP -= self.radiation_strength/100

    def loop(self):
        NFC_thread = Thread(target=NFC_reading, args=[])
        NFC_thread.start()
        while True:
            while not self.game_ended():
                try:
                    print("cycle")
                    self.handle_network()
                    self.HPBar.display(self.HP)
                    self.check_NFC()
                    self.handle_state()
                    self.check_game()
                    self.update_HP()
                except Exception as e:
                    traceback.print_exc()
                    print('Exception', str(e))
                time.sleep(0.1)
            self.check_NFC()


if __name__ == "__main__":
    dm = DosimeterMock()
    dm.loop()
