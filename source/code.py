import time
import gc
from monster import Monster
from ui import Ui
from inputctrl import InputCtrl
import json
import gc

monster = None
currUi = None
monData = None
currSave = None

def initialize():
    global monster,currUi,monData
    load()
    if not monster:
        monster = Monster("Chills",4,4,4,0,0,0,0,2,0,0,0,0,0,time.time(),time.time(),time.time(),"Chills2",32)
    currUi = Ui(monster)

def save():
    pass

def load():
    global monData,currSave,monster
    dataFile = open("monData.json")
    monData = json.load(dataFile)
    saveFile = open("save.json")
    currSave = json.load(saveFile)
    dataFile.close()
    saveFile.close()
    for monEntry in monData:
        if monEntry['name'] == currSave[0]['name']:
           monster = Monster(name=monEntry['name'],power=monEntry['power'],monType=monEntry['monType'],evoStage=monEntry['evoStage'],evolvesTo=monEntry['evolvesTo'],resolution=monEntry['resolution'],ageToEvo=monEntry['resolution'],hunger=currSave[0]['hunger'],strength=currSave[0]['strength'],effort=currSave[0]['effort'],age=currSave[0]['age'],weight=currSave[0]['hunger'],numPoop=currSave[0]['numPoop'],overFeeds=currSave[0]['overFeeds'],sickness=currSave[0]['sickness'],injury=currSave[0]['injury'],timeSinceEat=currSave[0]['timeSinceEat'],timeSinceTrain=currSave[0]['timeSinceTrain'],timeSincePoop=currSave[0]['timeSincePoop'])

# Load or create new data
initialize()

# Game loop
while True:
    monster.update()
    currUi.update()
    gc.collect()
    #print(gc.mem_free())
    time.sleep(1/15)
