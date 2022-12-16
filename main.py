#import libraries
import RPi.GPIO as GPIO
import time
import network_scanner
import sys

address = sys.argv[1]

#GPIO Basic initialization
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

led1 = 4
led2 = 17
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

while True:
    
    strength = -network_scanner.get_signal_strength(address)
    print(strength)
    GPIO.output(led1, strength < 30)
    GPIO.output(led2, strength < 50)
    time.sleep(1)
