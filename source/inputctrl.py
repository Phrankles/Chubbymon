import digitalio
import keypad
import time
import board

class InputCtrl:

    def __init__(self):
        self.keys = keypad.Keys([board.GP15,board.GP17,board.GP2,board.GP3],value_when_pressed=False, pull=True)

    def getInput(self):
        return self.keys.events.get()

class MainInputControl(InputCtrl):

    def __init__(self):
        super().__init__()
        self.selectIdx = 0

    def incIdx(self):
        if self.selectIdx < 10:
            self.selectIdx += 1
        else:
            self.selectIdx = 0

    def decIdx(self):
        if self.selectIdx == 0:
            self.selectIdx = 10
        elif self.selectIdx > 0:
            self.selectIdx -= 1



