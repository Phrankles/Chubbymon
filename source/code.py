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
    monster = Monster("Chills",0,0,0,0,0,0,0,0,0,0,0,0,time.time(),time.time(),time.time())
    currUi = Ui(monster)

def save():
    pass

def updateMonster():

    # Update things that happen each sec
    global secTime
    deltaTime = time.time() - secTime
    if deltaTime >= 1:
        monster.incAge(deltaTime)
        secTime = time.time()

    # Update things that happen each min
    global minTime
    if (time.time() - minTime) >= 60:
        save()
        minTime = time.time()

# Load or create new data
initialize()

# Game loop
while True:
    updateMonster()
    currUi.update()
    time.sleep(1/15)
