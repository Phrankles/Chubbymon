import digitalio
import keypad
import time
import board

class InputCtrl:

    def __init__(self,keys,timeSinceInput):
        self.keys = keys
        self.timeSinceInput = timeSinceInput
        self.enabled = True

    def getInput(self):
        if self.keys:
            return self.keys.events.get()
        else:
            return None

class MainInputControl(InputCtrl):

    def __init__(self,keys,timeSinceInput):
        super().__init__(keys,timeSinceInput)
        self.selectIdx = 0
        self.feedIdx = 0

    def incSelectIdx(self):
        if self.enabled:
            if self.selectIdx < 9:
                self.selectIdx += 1
            else:
                self.selectIdx = 0

    def decSelectIdx(self):
        if self.enabled:
            if self.selectIdx == 0:
                self.selectIdx = 9
            elif self.selectIdx > 0:
                self.selectIdx -= 1

    def incFeedIdx(self):
        if self.feedIdx == 0:
            self.feedIdx =1
        else:
            self.feedIdx = 0

    def decFeedIdx(self):
        if self.feedIdx == 0:
            self.feedIdx =1
        else:
            self.feedIdx = 0

    def zeroIdxs(self):
        self.feedIdx = 0
        self.selectIdx = 0

class TrainInputControl(InputCtrl):

    def __init__(self,keys,timeSinceInput):
        super().__init__(keys,timeSinceInput)
        self.selectIdx = 0

    def incSelectIdx(self):
        if self.enabled:
            if self.selectIdx < 2:
                self.selectIdx += 1
            else:
                self.selectIdx = 0

    def decSelectIdx(self):
        if self.enabled:
            if self.selectIdx == 0:
                self.selectIdx = 2
            elif self.selectIdx > 0:
                self.selectIdx -= 1
                