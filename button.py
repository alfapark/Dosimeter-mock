import RPi.GPIO as GPIO
import time 


class Button:
    def __init__(self, pin):
        self.btn_pin = pin
        GPIO.setup(self.btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_hold(self):
        return GPIO.input(self.btn_pin) == GPIO.HIGH

if __name__ == "__main__":
    btn = Button(17)
    while True: # Run forever
        if btn.is_hold():
            print("Button was pushed!")
        time.sleep(1)
