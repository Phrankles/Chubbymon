#UI class

import displayio
from picolcd import PicoLCD
from monster import Monster
import time
import storage
from inputctrl import MainInputControl,TrainInputControl,TrainStrInputControl,TrainIntInputControl
import alarm
import board
import keypad

from screen import IdleScreen,StatusScreen,TrainScreen,BattleScreen,LightsScreen,MedicalScreen,JournalScreen,ConnectScreen,StrGameScreen,IntGameScreen

from audioctrl import AudioCtrl

class Ui:

    def __init__(self,monster):

        self.keys = keypad.Keys([board.GP15,board.GP17,board.GP2,board.GP3],value_when_pressed=False, pull=True)
        self.inputCtrl = MainInputControl(self.keys,time.monotonic())
        self.enabled = True
        self.monster = monster
        self.currScreen = IdleScreen(self.monster,self.inputCtrl)

        # Initialize the LCD
        self.LCD = PicoLCD()
        self.display = self.LCD.returnLCD()

    def update(self):
        #screen transitions
    	if self.currScreen.transition == "status":
            self.inputCtrl = MainInputControl(self.keys,self.inputCtrl.timeSinceInput)
            self.currScreen.destroy()
            self.currScreen = StatusScreen(self.monster,self.inputCtrl)
    	elif self.currScreen.transition == "train":
            self.inputCtrl = TrainInputControl(self.keys,self.inputCtrl.timeSinceInput)
            self.currScreen.destroy()
            self.currScreen = TrainScreen(self.monster,self.inputCtrl)
    	elif self.currScreen.transition == "idle":
            self.inputCtrl = MainInputControl(self.keys,self.inputCtrl.timeSinceInput)
            self.currScreen.destroy()
            self.currScreen = IdleScreen(self.monster,self.inputCtrl)
        elif self.currScreen.transition == "str-game":
            self.inputCtrl = TrainStrInputControl(self.keys,self.inputCtrl.timeSinceInput)
            self.currScreen.destroy()
            self.currScreen = StrGameScreen(self.monster,self.inputCtrl)
        elif self.currScreen.transition == "int-game":
            self.inputCtrl = TrainIntInputControl(self.keys,self.inputCtrl.timeSinceInput)
            self.currScreen.destroy()
            self.currScreen = IntGameScreen(self.monster,self.inputCtrl)

        # "sleep"
        if (self.inputCtrl.timeSinceInput + 15) < time.monotonic() and self.enabled:
        	self.disable()
        if (self.inputCtrl.timeSinceInput + 15) > time.monotonic() and not self.enabled:
        	self.enable()
        if self.enabled:    	
        	self.display.show(self.currScreen.main)


        self.currScreen.update()

    def disable(self):

        self.LCD.releaseLCD()
    	self.currScreen.destroy()  
        self.inputCtrl = MainInputControl(self.keys,self.inputCtrl.timeSinceInput) 	
    	self.currScreen = IdleScreen(self.monster,self.inputCtrl)
    	self.currScreen.update()
    	self.display.show(self.currScreen.main)
        self.enabled = False
        self.inputCtrl.enabled = False

    def enable(self):
        self.enabled = True
        self.inputCtrl.enabled = True
        self.inputCtrl.timeSinceInput = time.monotonic()
        self.inputCtrl.zeroIdxs()
        self.LCD.reinitLCD()

