# Dosimeter mock

A game device for outside game. Explore your surroundings, find goals, hide from radiation with a dosimeter device.

## Documentation

Documentation is provided in `documents/main.tex`, compile it with your LaTeX compiler.

## Components
- RaspberryPi 4 B
- 4 Digit Display V1.2 (HW-069) 
- RFID-RC522
- Powerbank

## Pins
- 4 Digit Display V1.2 (HW-069)
  - CLK - GPIO 3 (5)
  - DIO - GPIO 2 (3)
  - VCC - 3.3V (1)
  - GND - GND(6)
- RFID-RC522
  - SDA - GPIO 8 (24)
  - SCK - GPIO 11 (23)
  - MOSI - GPIO 10 (19)
  - MISO - GPIO 9 (21)
  - IRQ - Not used
  - GND - GND (20)
  - RST - GPIO 25 (22)
  - 3.3V - 3.3V (17)
- Button
 - Power - 5V (4)
 - Detect - GPIO 4 (7)
- LEDS
  - L1 - GPIO 5 (29)
  - L2 - GPIO 6 (31)
  - L3 - GPIO 13 (33)
  - L4 - GPIO 19 (35)
  - L5 - GPIO 26 (37)
  - L6 - GPIO 20 (38)
  - Status - GPIO 21 (40)
  - Radiation - GPIO 16 (36)
  - GND - GND (39)
