#UI class

import displayio
from adafruit_bitmapsaver import save_pixels
from picolcd import PicoLCD
from monster import Monster
import time
import storage

from screen import IdleScreen,StatusScreen,FeedScreen,TrainScreen,BattleScreen,LightsScreen,MedicalScreen,JournalScreen,ConnectScreen

from audioctrl import AudioCtrl

class Ui:

    def __init__(self,monster):
        #storage.remount("/", False)
        self.enabled = True
        self.monster = monster
        self.currScreen = IdleScreen(monster)
        # Initialize the LCD
        self.LCD = PicoLCD()
        self.display = self.LCD.returnLCD()

    def update(self):
        if self.enabled:
            self.display.show(self.currScreen.main)
            self.currScreen.update()
            #save_pixels('screenshots/image' + str(time.time()) + ".bmp", self.display)

    def disable(self):
        self.enabled = False
        self.LCD.releaseLCD()

    def enable(self):
        self.enabled = True
        self.LCD.reinitLCD()

