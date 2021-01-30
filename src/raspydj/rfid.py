from mfrc522 import SimpleMFRC522
class RFID:
    def __init__(self):
        self.reader = SimpleMFRC522()
