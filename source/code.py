import time
import gc
from monster import Monster
from ui import Ui
from inputctrl import InputCtrl

monster = None
currUi = None

# Create timers
secTime = time.time()
minTime = time.time()

def initialize():
    global monster,currUi
    monster = Monster("Chills",4,4,4,0,0,0,0,0,0,0,0,0,time.time(),time.time(),time.time())
    currUi = Ui(monster)

def save():
    pass

def load():
    pass

# Load or create new data
initialize()

# Game loop
while True:
    monster.update()
    currUi.update()
    time.sleep(1/15)
