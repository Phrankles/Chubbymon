# Monster class

import time
import adafruit_imageload
import displayio

class Monster:

    def __init__(self,name,hunger,strength,effort,power,age,weight,monType,evoStage,numPoop,overFeeds,sickness,injury,ageToEvo,timeSinceEat,timeSinceTrain,timeSincePoop,evolvesTo,resolution):
        self.name = name
        self.hunger = hunger
        self.strength = strength
        self.power = power
        self.effort = effort
        self.age = age
        self.weight = weight
        self.monType = monType
        self.evoStage = evoStage
        self.numPoop = numPoop
        self.overFeeds = overFeeds
        self.sickness = sickness
        self.injury = injury
        self.ageToEvo = ageToEvo
        self.timeSinceEat = timeSinceEat
        self.timeSinceTrain = timeSinceTrain
        self.timeSincePoop = timeSincePoop
        self.evolvesTo = evolvesTo
        self.resolution = resolution

        self.monSheet, self.monPalette = adafruit_imageload.load(
            "/sprites/" + self.name + "/" + self.name + ".bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.monPalette.make_transparent(0)
        self.monSprite = displayio.TileGrid(
            self.monSheet, pixel_shader=self.monPalette, width=1, height=1, tile_width=self.resolution, tile_height=self.resolution
        )

        self.idleBgSheet, self.idleBgPalette = adafruit_imageload.load(
            "/sprites/" + self.name + "/" + self.name + "_bg.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.idleBgSprite = displayio.TileGrid(
            self.idleBgSheet, pixel_shader=self.idleBgPalette, width=1, height=1, tile_width=120, tile_height=68
        )

    def incHunger(self):
        if self.hunger < 4:
            self.hunger += 1

    def decHunger(self):
        self.hunger -= 1

    def incStrength(self):
        if self.strength < 4:
            self.strength += 1

    def decStrength(self):
        self.strength -= 1

    def incPower(self):
        self.power += 1

    def decPower(self):
        self.power -= 1

    def incEffort(self):
        self.effort += 1

    def decEffort(self):
        self.effort -= 1

    def cleanPoop(self):
        self.numPoop = 0

    def resetPoop(self):
        self.numPoop = 0

    def incAge(self,secs):
        self.age += secs

    def incTimeSinceEat(self,secs):
        self.timeSinceEat += secs

    def resetTimeSinceEat(self):
        self.timeSinceEat = 0

    def incTimeSinceTrain(self,secs):
        self.timeSinceTrain += secs

    def resetTimeSinceTrain(self):
        self.timeSinceTrain = 0

    def incTimeSincePoop(self,secs):
        self.timeSincePoop += secs

    def resetTimeSincePoop(self):
        self.timeSincePoop = 0

    def feedMeat(self):
        if self.hunger < 4:
            self.hunger += 1
            self.weight += 1
        else:
            self.overFeed()

    def feedProtien(self):
        if self.strength < 4:
            self.strength += 1
            self.weight += 2
        else:
            self.overFeed()

    def overFeed(self):
        self.overFeeds += 1
        self.weight += 1

    def update(self):
        self.checkInjury()
        self.checkSick()
        self.checkPoop()
        self.checkWeight()

        self.consumeHunger()
        self.consumeStrength()

    def checkInjury(self):
        if self.injury > 3:
            self.die()

    def checkSick(self):
        if self.sickness > 3:
            self.die()

    def checkPoop(self):
        if (time.time() - self.timeSincePoop) > 2:
            if self.numPoop <= 4:
                self.numPoop += 1
                self.timeSincePoop = time.time()
            else:
                self.sickness += 1
                self.timeSincePoop = time.time()

    def checkWeight(self):
        if self.weight > 99:
            self.injury += 1
            self.weight = 99
        elif self.weight < 10:
            self.weight = 10

    def consumeHunger(self):
        if (time.time() - self.timeSinceEat) > 100:
            if self.hunger > 0:
                self.hunger -= 1
                self.timeSinceEat = time.time()
            else:
                self.injury += 1
                self.timeSinceEat = time.time()

        pass

    def consumeStrength(self):
        if (time.time() - self.timeSinceTrain) > 100:
            if self.strength > 0:
                self.strength -= 1
                self.timeSinceTrain = time.time()
            else:
                self.injury += 1
                self.timeSinceTrain = time.time()

    def die(self):
        self.sickness = 0
        self.injury = 0

    def isHappy(self):
        if self.hunger == 4 and self.strength == 4:
            return True
        return False

    def isContent(self):
        if self.hunger > 1 and self.strength > 1:
            return True
        return False

    def isMad(self):
        if self.hunger <= 1 or self.strength <= 1:
            return True
        return False
