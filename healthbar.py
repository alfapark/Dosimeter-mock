import RPi.GPIO as GPIO

class HealthBar:
    def __init__(self, pins, maxval = 100):
        self.pins = pins
        self.maxval = maxval
        for pin in self.pins:
            GPIO.setup(pin,GPIO.OUT)

    def display(self, value):
        step = self.maxval/value
        for i in range(len(self.pins)):
            GPIO.output(self.pins[i], value >= i*step)
