import tm1637
import time

class Display:
    def __init__(self, clk_pin, dio_pin):
        self.tm = tm1637.TM1637(clk=clk_pin, dio=dio_pin)
        self.start_time = time.time()

    def display_time(self):
        elapsed = time.time()
        elapsed -= self.start_time
        minutes, seconds = int(elapsed//60), int(elapsed) % 60 
        self.tm.numbers(minutes, seconds)

    def display_number(self, letter, number):
        number = int(number)
        chars = letter + str(number).zfill(3)
        self.tm.show(chars)

    def display_text(self, text):
        self.tm.show(text)


if __name__ == "__main__":
    # all LEDS on "88:88"
    tm.write([127, 255, 127, 127])
    time.sleep(1)
    # all LEDS off
    tm.write([0, 0, 0, 0])
    time.sleep(1)
    # show "0123"
    tm.write([63, 6, 91, 79])
    time.sleep(1)
    # show "COOL"
    tm.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
    time.sleep(1)
    # show "HELP"
    tm.show('help')
    time.sleep(1)
    # display "dEAd", "bEEF"
    tm.hex(0xdead)
    tm.hex(0xbeef)
    time.sleep(1)
    # show "-123"
    tm.number(-123)
    time.sleep(1)
    # show temperature '24*C'
    tm.temperature(24)

