import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


class Reader:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def read(self):
        id, text =self.reader.read()
        return id,text

if __name__ == "__main__":
    reader = Reader()
    id, text = reader.read()
    print(id)
    print(text)
