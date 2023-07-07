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

class State(Enum):
    RADIATION = 1
    TIME = 2
    HEALTH = 3
    GOAL_DISTANCE = 4
    SHIELD = 5
    FINISHED = 10
    DEAD = 11

next_state = {
    State.FINISHED: State.FINISHED,
    State.DEAD: State.DEAD,
    State.RADIATION : State.TIME,
    State.TIME : State.HEALTH,
    State.HEALTH : State.GOAL_DISTANCE,
    State.GOAL_DISTANCE : State.SHIELD,
    State.RADIATION : State.RADIATION,
}

class DosimeterMock:
    def __init__(self):
        self.set_initial_state()
        #GPIO Basic initialization
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

        self.status_led_pin = 21
        GPIO.setup(self.status_led_pin,GPIO.OUT)
        self.radiation_led_pin = 16
        GPIO.setup(self.radiation_led_pin,GPIO.OUT)

        leds = [20,26,19,13,6,5]
        self.HPBar = HealthBar(leds, maxval=self.HP)

        self.display = Display(clk_pin=3, dio_pin=2)

        self.button = Button(4)
        self.button_hold_last_time = False

        self.parse_config()

        self.NFC_MSG = None        
        self.WIFI_signals = dict()

        self.status_time = time.time()
        self.shield_time = time.time()
        self.last_radiation_up = time.time()

    def parse_config(self):
        try:
            config_dict = load_json_file("config.json")
            self.goal_address = config_dict["goal_adr"]
            self.radiation_addresses = config_dict["radiation_adrs"]
        except:
            self.goal_address = "invalid"
            self.radiation_addresses = []

    def set_initial_state(self):
        self.state = State.GOAL_DISTANCE
        self.radiation_strength = 0
        self.goal_distance = 100
        self.HP = 100
        self.start = time.time()

    def status_led_up(self):
        GPIO.output(self.status_led_pin, True)
        self.status_time = time.time() + 0.2

    def update_status_led(self):
        if self.status_time < time.time():
            GPIO.output(self.status_led_pin, False)

    def update_radiation_led(self):
        if self.last_radiation_up > time.time() + 0.2:
            GPIO.output(self.radiation_led_pin, False)
        diff = (time.time() - self.last_radiation_up)
        if diff/self.radiation_strength < 0.05:
            GPIO.output(self.radiation_led_pin, True)
            self.last_radiation_up = time.time()

    def get_elapsed_seconds(self):
        elapsed = time.time() - self.start
        return int(elapsed)

    def check_NFC(self):
        msg = self.NFC_MSG
        self.NFC_MSG = None
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
        elif msg == "SHIELD":
            self.shield_time = time.time() + 30

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
        elif self.state == State.SHIELD:
            self.display.display_number('S', max(self.shield_time-time.time(), 0))
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
        signals = self.WIFI_signals
        self.goal_distance = 999
        self.radiation_strength = 0
        for address in signals:
            if address in self.radiation_addresses or signals[address]['ESSID'] == '"DM-radiation"':
                self.radiation_strength += network_scanner.parse_signal_strength(signals[address]) + 100
            if self.goal_address == address or signals[address]['ESSID'] == '"DM-goal"':
                self.goal_distance = -network_scanner.parse_signal_strength(signals[address])

    def update_HP(self):
        if self.shield_time < time.time():
            self.HP -= self.radiation_strength/1000

    def loop(self):
        NFC_thread = Thread(target=self.NFC_reading, args=[])
        NFC_thread.start()
        WIFI_thread = Thread(target=self.WIFI_reading, args=[])
        WIFI_thread.start()
        while True:
            while not self.game_ended():
                try:
                    print("cycle")
                    self.update_status_led()
                    self.update_radiation_led()
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
            self.status_led_up()
            self.check_NFC()
            time.sleep(0.1)


    def NFC_reading(self):
        reader = Reader()
        while True:
            id,text = reader.read()
            self.status_led_up()
            print(id, text)
            self.NFC_MSG = text
            time.sleep(1)


    def WIFI_reading(self):
        while True:
            WIFI_signals = network_scanner.parse_interface()
            self.WIFI_signals = WIFI_signals
            time.sleep(1)


if __name__ == "__main__":
    dm = DosimeterMock()
    dm.loop()
