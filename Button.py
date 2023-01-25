import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

btn_pin = 17

GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True: # Run forever
    if GPIO.input(btn_pin) == GPIO.HIGH:
        print("Button was pushed!")
    time.sleep(1)
