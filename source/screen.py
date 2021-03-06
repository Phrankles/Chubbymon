#Screen class

import time
import displayio
import adafruit_imageload
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect
from characteranimator import CharacterAnimator
from adafruit_display_text import label
import terminalio
from inputctrl import MainInputControl
from keypad import Event
from comm import Comm
import gc
import random
import simpleio
import board

A_EVENT = Event(0, True)
B_EVENT = Event(1, True)
C_EVENT = Event(2, True)
D_EVENT = Event(3, True)

class Screen:

    def __init__(self,monster,inputCtrl):

        self.monster = monster
        self.inputCtrl = inputCtrl

        self.charAnimator = CharacterAnimator(self.monster,self.inputCtrl)

        self.main = displayio.Group(scale=1)

        self.transition = None

    def destroy(self):
        try:
            self.main.remove(self.monster.monSprite)
        except ValueError:
            pass           
        try:
            self.main.remove(self.monster.idleBgSprite)
        except ValueError:
            pass 
        gc.collect()

    def handleInput(self):
        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                self.transition = "idle"
            elif self.input == B_EVENT:
                self.transition = "idle"
            elif self.input == D_EVENT:
                self.transition = "idle"
            elif self.input == C_EVENT:
                self.transition = "idle"

    def update(self):
        self.handleInput()

class IdleScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster,inputCtrl)

        #Select Tile Grid load
        self.selectSheet, self.selectPalette = adafruit_imageload.load(
            "/sprites/select.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.selectPalette.make_transparent(0)
        self.selectPalette.make_transparent(1)
        self.selectPalette.make_transparent(2)
        self.selectPalette.make_transparent(3)
        self.selectSprite = displayio.TileGrid(
            self.selectSheet, pixel_shader=self.selectPalette, width=1, height=1, tile_width=32, tile_height=32
        )

        self.inputCtrl = inputCtrl
        self.input = None

        self.subMenuOpen = False
        self.subMenu = None

        #Idle Menu Sprite load
        self.statusSheet, self.statusPalette = adafruit_imageload.load(
            "/sprites/status.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.feedSheet, self.feedPalette = adafruit_imageload.load(
            "/sprites/feed.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.trainSheet, self.trainPalette = adafruit_imageload.load(
            "/sprites/train.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.battleSheet, self.battlePalette = adafruit_imageload.load(
            "/sprites/battle.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.pooSheet, self.pooPalette = adafruit_imageload.load(
            "/sprites/poo.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.lightsSheet, self.lightsPalette = adafruit_imageload.load(
            "/sprites/lights.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.medicineSheet, self.medicinePalette = adafruit_imageload.load(
            "/sprites/medicine.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.journalSheet, self.journalPalette = adafruit_imageload.load(
            "/sprites/journal.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.linkSheet, self.linkPalette = adafruit_imageload.load(
            "/sprites/link.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.callSheet, self.callPalette = adafruit_imageload.load(
            "/sprites/call.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )

        #Set transparency index
        self.statusPalette.make_transparent(0)
        self.feedPalette.make_transparent(0)
        self.trainPalette.make_transparent(0)
        self.battlePalette.make_transparent(0)
        self.pooPalette.make_transparent(0)
        self.lightsPalette.make_transparent(0)
        self.medicinePalette.make_transparent(0)
        self.journalPalette.make_transparent(0)
        self.linkPalette.make_transparent(0)
        self.callPalette.make_transparent(0)


        self.statusSprite = displayio.TileGrid(
            self.statusSheet, pixel_shader=self.statusPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.feedSprite = displayio.TileGrid(
            self.feedSheet, pixel_shader=self.feedPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.trainSprite = displayio.TileGrid(
            self.trainSheet, pixel_shader=self.trainPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.battleSprite = displayio.TileGrid(
            self.battleSheet, pixel_shader=self.battlePalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.pooSprite = displayio.TileGrid(
            self.pooSheet, pixel_shader=self.pooPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.lightsSprite = displayio.TileGrid(
            self.lightsSheet, pixel_shader=self.lightsPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.medicineSprite = displayio.TileGrid(
            self.medicineSheet, pixel_shader=self.medicinePalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.journalSprite = displayio.TileGrid(
            self.journalSheet, pixel_shader=self.journalPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.linkSprite = displayio.TileGrid(
            self.linkSheet, pixel_shader=self.linkPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.callSprite = displayio.TileGrid(
            self.callSheet, pixel_shader=self.callPalette, width=1, height=1, tile_width=32, tile_height=32
        )

        #Monster initial position
        self.monster.monSprite.x = 132 - int(self.monster.resolution/2)
        self.monster.monSprite.y = 100 - int(self.monster.resolution/2)
        # Icon positions main screen
        self.statusSprite.x = 20
        self.statusSprite.y = 2
        self.feedSprite.x = 62
        self.feedSprite.y = 2
        self.trainSprite.x = 104
        self.trainSprite.y = 1
        self.battleSprite.x = 146
        self.battleSprite.y = 2
        self.pooSprite.x = 188
        self.pooSprite.y = 2
        self.lightsSprite.x = 20
        self.lightsSprite.y = 100
        self.medicineSprite.x = 62
        self.medicineSprite.y = 100
        self.journalSprite.x = 104
        self.journalSprite.y = 100
        self.linkSprite.x = 146
        self.linkSprite.y = 100
        self.callSprite.x = 188
        self.callSprite.y = 100

        self.bgGroup = displayio.Group(scale=2)
        self.bgGroup.append(self.monster.idleBgSprite)


        self.selectGroup = displayio.Group(scale=1)
        self.selectGroup.append(self.selectSprite)

        self.iconGroup = displayio.Group(scale=1)
        self.iconGroup.append(self.statusSprite)
        self.iconGroup.append(self.feedSprite)
        self.iconGroup.append(self.trainSprite)
        self.iconGroup.append(self.battleSprite)
        self.iconGroup.append(self.pooSprite)
        self.iconGroup.append(self.lightsSprite)
        self.iconGroup.append(self.medicineSprite)
        self.iconGroup.append(self.journalSprite)
        self.iconGroup.append(self.linkSprite)
        self.iconGroup.append(self.callSprite)

        self.main.append(self.bgGroup)
        self.main.append(self.monster.monSprite)
        self.main.append(self.selectGroup)
        self.main.append(self.iconGroup)

    def update(self):
        if not self.subMenu:
            self.charAnimator.randomIdle()
        self.handleInput()
        self.updateSelPos()
        if self.subMenu:
            self.subMenu.update(self.input)

    def handleInput(self):
        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                if self.subMenuOpen:
                    pass
                else:
                    self.inputCtrl.incSelectIdx()
            elif self.input == B_EVENT:
                if not self.subMenuOpen:
                    self.inputCtrl.decSelectIdx()
            if self.input == D_EVENT:
                if self.subMenu:
                    self.main.remove(self.monster.monSprite)
                    self.main.pop()
                    self.subMenuOpen = False
                    self.subMenu = None
                    self.main.insert(1,self.monster.monSprite)
                elif not self.inputCtrl.selectIdx == 0:
                    self.inputCtrl.selectIdx = 0
            elif self.input == C_EVENT and not self.subMenu:
                self.perfAction(self.input)

    def perfAction(self,input):
        if self.inputCtrl.selectIdx == 1  and not self.subMenuOpen:
            self.transition = "status"
        elif self.inputCtrl.selectIdx == 2 and not self.subMenuOpen:
            self.subMenuOpen = True
            self.subMenu = FeedSubScreen(self.monster,self.charAnimator,self.main,self.inputCtrl)
        elif self.inputCtrl.selectIdx == 3 and not self.subMenuOpen:
            self.transition = "train"
        elif self.inputCtrl.selectIdx == 5 and not self.subMenuOpen:
            self.monster.numPoop = 0
            self.charAnimator.cleanPoop()
        elif self.inputCtrl.selectIdx == 9 and not self.subMenuOpen:
            comm = Comm()
            comm.execute("V1-836E-212E-288E-182E-018E-@800E")

    def updateSelPos(self):
        if self.inputCtrl.selectIdx != 0:
            try:
                self.main.append(self.selectGroup)
                self.main.append(self.iconGroup)
            except ValueError:
                pass
        if self.inputCtrl.selectIdx == 0:
            try:
                self.main.remove(self.iconGroup)
                self.main.remove(self.selectGroup)
            except ValueError:
                pass
        elif self.inputCtrl.selectIdx == 1:
            self.selectSprite.x = self.statusSprite.x
            self.selectSprite.y = self.statusSprite.y
        elif self.inputCtrl.selectIdx == 2:
            self.selectSprite.x = self.feedSprite.x
            self.selectSprite.y = self.feedSprite.y
        elif self.inputCtrl.selectIdx == 3:
            self.selectSprite.x = self.trainSprite.x
            self.selectSprite.y = self.trainSprite.y
        elif self.inputCtrl.selectIdx == 4:
            self.selectSprite.x = self.battleSprite.x
            self.selectSprite.y = self.battleSprite.y
        elif self.inputCtrl.selectIdx == 5:
            self.selectSprite.x = self.pooSprite.x
            self.selectSprite.y = self.pooSprite.y
        elif self.inputCtrl.selectIdx == 6:
            self.selectSprite.x = self.lightsSprite.x
            self.selectSprite.y = self.lightsSprite.y
        elif self.inputCtrl.selectIdx == 7:
            self.selectSprite.x = self.medicineSprite.x
            self.selectSprite.y = self.medicineSprite.y
        elif self.inputCtrl.selectIdx == 8:
            self.selectSprite.x = self.journalSprite.x
            self.selectSprite.y = self.journalSprite.y
        elif self.inputCtrl.selectIdx == 9:
            self.selectSprite.x = self.linkSprite.x
            self.selectSprite.y = self.linkSprite.y
        elif self.inputCtrl.selectIdx == 10:
            self.selectSprite.x = self.callSprite.x
            self.selectSprite.y = self.callSprite.y

    def destroy(self):
        self.main.remove(self.monster.monSprite)
        self.bgGroup.remove(self.monster.idleBgSprite)
        for item in self.main:
            self.main.pop()
        gc.collect()

class StatusScreen(Screen):

    def __init__(self, monster,inputCtrl):

        super().__init__(monster,inputCtrl)

        self.menuBgSheet,self.menuBgPalette = adafruit_imageload.load(
            "/sprites/menu_bg.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )

        self.menuBgSprite = displayio.TileGrid(
            self.menuBgSheet, pixel_shader=self.menuBgPalette, width=1, height=1, tile_width=120, tile_height=68
        )

        self.nameArea = label.Label(terminalio.FONT, text="Name: " + self.monster.name, color=0xFFFFFF)
        self.nameArea.x = 5
        self.nameArea.y =10

        self.ageArea = label.Label(terminalio.FONT, text="Age: " + str(int(self.monster.age/86400)) + "y", color=0xFFFFFF)
        self.ageArea.x = 5
        self.ageArea.y =20

        self.weightArea = label.Label(terminalio.FONT, text="Weight: " + str(self.monster.weight) + "g", color=0xFFFFFF)
        self.weightArea.x = 55
        self.weightArea.y =20

        self.hungerArea = label.Label(terminalio.FONT, text="Hunger: " + str(self.monster.hunger), color=0xFFFFFF)
        self.hungerArea.x = 5
        self.hungerArea.y =30

        self.strengthArea = label.Label(terminalio.FONT, text="Strength: " + str(self.monster.strength), color=0xFFFFFF)
        self.strengthArea.x = 5
        self.strengthArea.y =40

        self.effortArea = label.Label(terminalio.FONT, text="Effort: " + str(self.monster.effort), color=0xFFFFFF)
        self.effortArea.x = 5
        self.effortArea.y =50

        self.charAnimator.monSprite.x = 190 - int(self.monster.resolution/2)
        self.charAnimator.monSprite.y = 100 - int(self.monster.resolution/2)

        self.statsGroup = displayio.Group(scale=2)
        self.statsGroup.append(self.monster.idleBgSprite)
        self.statsGroup.append(self.nameArea)
        self.statsGroup.append(self.ageArea)
        self.statsGroup.append(self.weightArea)
        self.statsGroup.append(self.hungerArea)
        self.statsGroup.append(self.strengthArea)
        self.statsGroup.append(self.effortArea)
        try:            
            self.main.append(self.statsGroup)
            self.main.append(self.charAnimator.monSprite)
        except ValueError:
            pass

    def update(self):
        self.handleInput()
        self.charAnimator.simpleIdle()

    def destroy(self):
        self.statsGroup.remove(self.monster.idleBgSprite)
        self.main.remove(self.monster.monSprite)
        for item in self.main:
            self.main.pop()

class FeedSubScreen():

    def __init__(self, monster, charAnimator, main, inputCtrl):

        self.monster = monster

        self.charAnimator = charAnimator
        self.main = main

        self.inputCtrl = inputCtrl

        self.ready = False

        self.selSheet, self.selPalette = adafruit_imageload.load(
            "/sprites/select.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.selPalette.make_transparent(0)
        self.selPalette.make_transparent(1)
        self.selPalette.make_transparent(2)
        self.selPalette.make_transparent(3)
        self.selSprite = displayio.TileGrid(
            self.selSheet, pixel_shader=self.selPalette, width=1, height=1, tile_width=32, tile_height=32
        )

        self.meatSheet, self.meatPalette = adafruit_imageload.load(
            "/sprites/meat.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.meatPalette.make_transparent(0)
        self.meatSprite = displayio.TileGrid(
            self.meatSheet, pixel_shader=self.meatPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.meatSprite.x = 20
        self.meatSprite.y = 18

        self.protienSheet, self.protienPalette = adafruit_imageload.load(
            "/sprites/protien.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.protienPalette.make_transparent(0)
        self.protienSprite = displayio.TileGrid(
            self.protienSheet, pixel_shader=self.protienPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.protienSprite.x = 70
        self.protienSprite.y = 18

        self.selSprite.x = self.meatSprite.x
        self.selSprite.y = self.meatSprite.y

        foodGroup = displayio.Group(scale=2)
        try:
            foodGroup.append(self.selSprite)
            foodGroup.append(self.meatSprite)
            foodGroup.append(self.protienSprite)
        except ValueError:
            pass

        self.main.append(foodGroup)

    def update(self, input):
        if not self.ready:
            self.ready = True
        else:
            self.handleInput(input)
        self.updateSelPos()
        self.charAnimator.randomIdle()

    def handleInput(self,input):

        if input:
            if input == A_EVENT:
                self.inputCtrl.incFeedIdx()
            elif input == B_EVENT:
                self.inputCtrl.decFeedIdx()
            elif input == C_EVENT:
                self.perfAction()

    def updateSelPos(self):
        if self.inputCtrl.feedIdx == 0:
            self.selSprite.x = self.meatSprite.x
            self.selSprite.y = self.meatSprite.y
        else:
            self.selSprite.x = self.protienSprite.x
            self.selSprite.y = self.protienSprite.y

    def perfAction(self):
        if self.inputCtrl.feedIdx == 0:
            self.monster.feedMeat()
            temp = self.main.pop()
            temp2 = self.main.pop()
            temp3 = self.main.pop()
            self.main.append(self.charAnimator.animLayer)
            self.charAnimator.feedMeat()
            self.main.pop()
            self.main.append(temp3)
            self.main.append(temp2)
            self.main.append(temp)
        else:
            self.monster.feedProtien()
            temp = self.main.pop()
            temp2 = self.main.pop()
            temp3 = self.main.pop()
            self.main.append(self.charAnimator.animLayer)
            self.charAnimator.feedProtein()
            self.main.pop()
            self.main.append(temp3)
            self.main.append(temp2)
            self.main.append(temp)
        pass

class TrainScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

        self.strLabel = label.Label(terminalio.FONT, text="Strength", color=0xFF0F00)
        self.spdLabel = label.Label(terminalio.FONT, text="Speed", color=0xFFFFFF)
        self.intLabel = label.Label(terminalio.FONT, text="Intellect", color=0xFFFFFF)


        self.strLabel.y = 15
        self.strLabel.x = 10
        self.spdLabel.y = 30
        self.spdLabel.x = 10
        self.intLabel.y = 45
        self.intLabel.x = 10

        self.charAnimator.monSprite.x = 190 - int(self.monster.resolution/2)
        self.charAnimator.monSprite.y = 100 - int(self.monster.resolution/2)

        self.labelGroup = displayio.Group(scale=2)

        self.labelGroup.append(self.strLabel)
        self.labelGroup.append(self.spdLabel)
        self.labelGroup.append(self.intLabel)

        self.main.append(self.labelGroup)
        self.main.append(self.monster.monSprite)

    def handleInput(self):
        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                self.inputCtrl.incSelectIdx()
            elif self.input == B_EVENT:
                self.inputCtrl.decSelectIdx()
            elif self.input == D_EVENT:
                self.transition = "idle"
            elif self.input == C_EVENT:
                self.perfAction()

    def update(self):
        self.handleInput()
        self.updateSelPos()
        self.charAnimator.simpleIdle()

    def updateSelPos(self):

        if self.inputCtrl.selectIdx == 0:
            self.strLabel.color = 0xFF0F00
            self.spdLabel.color = 0xFFFFFF
            self.intLabel.color = 0xFFFFFF
        elif self.inputCtrl.selectIdx == 1:
            self.strLabel.color = 0xFFFFFF
            self.spdLabel.color = 0xFF0F00
            self.intLabel.color = 0xFFFFFF
        else:
            self.strLabel.color = 0xFFFFFF
            self.spdLabel.color = 0xFFFFFF
            self.intLabel.color = 0xFF0F00

    def perfAction(self):

        if self.inputCtrl.selectIdx == 0:
            self.transition = "str-game"
        elif self.inputCtrl.selectIdx == 1:
            self.transition = "spd-game"
        else:
            self.transition = "int-game"

class BattleScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class BattleScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class LightsScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class MedicalScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class JournalScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class ConnectScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

class StrGameScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)


        self.main.append(self.monster.monSprite)

    def update(self):
        self.handleInput()

    def handleInput(self):

        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                pass
            elif self.input == B_EVENT:
                pass
            elif self.input == D_EVENT:
                pass
            elif self.input == C_EVENT:
                pass

class IntGameScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

        self.showRules = True
        self.rules1 = label.Label(terminalio.FONT, text="Memorize the pattern", color=0xFF0F00)
        self.rules2 = label.Label(terminalio.FONT, text="Repeat the pattern", color=0xFF0F00)
        self.rules3 = label.Label(terminalio.FONT, text="to score!", color=0xFF0F00)

        self.rules1.y = 15
        self.rules2.y = 35
        self.rules2.x = 8
        self.rules3.y = 50
        self.rules3.x = 30

        self.rulesGroup = displayio.Group(scale=2)
        self.rulesGroup.append(self.rules1)
        self.rulesGroup.append(self.rules2)
        self.rulesGroup.append(self.rules3)

        self.gameGroup = displayio.Group(scale=1)

        self.topLeftRect = RoundRect(0,0,120,68,12,fill=0xFEFFD1,outline=0x000000)
        self.topRightRect = RoundRect(120,0,120,68,12,fill=0xAEBDFF,outline=0x000000)
        self.botRightRect = RoundRect(120,68,120,68,12,fill=0xB4FFC4,outline=0x000000)
        self.botLeftRect = RoundRect(0,68,120,68,12,fill=0xFFA1A1,outline=0x000000)

        self.gameGroup.append(self.topLeftRect)
        self.gameGroup.append(self.topRightRect)
        self.gameGroup.append(self.botRightRect)
        self.gameGroup.append(self.botLeftRect)
        self.gameGroup.append(self.monster.monSprite)

        self.pattern = [random.randint(0,3)]
        self.patternPlayed = False

        self.score = 0

        self.inputIdx = 0

        self.completedPattern = False

        self.gameOver = False

        self.main.append(self.rulesGroup)

    def update(self):
        if not self.gameOver:
            self.handleInput()
        else:
            self.endGame()

    def endGame(self):

        self.gameGroup.remove(self.monster.monSprite)
        endText1 = label.Label(terminalio.FONT, text="Game Over!", color=0xFF0F00)
        endText2 = label.Label(terminalio.FONT, text="Score: " + str(self.score), color=0xFF0F00)
        endText1.y = 15
        endText2.y = 35
        self.rulesGroup.remove(self.rules1)
        self.rulesGroup.remove(self.rules2)
        self.rulesGroup.remove(self.rules3)
        self.rulesGroup.append(endText1)
        self.rulesGroup.append(endText2)
        self.main.remove(self.gameGroup)
        self.main.append(self.rulesGroup)
        time.sleep(4)
        self.transition = "idle"

    def handleInput(self):

        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                    self.playPattern()
                else:
                    pass
            elif self.input == B_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                    self.playPattern()
                else:
                    pass
            elif self.input == D_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                    self.playPattern()
                else:
                    pass
            elif self.input == C_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                    self.playPattern()
                else:
                    pass

        if self.patternPlayed and not self.completedPattern:
            self.charAnimator.simpleIdle()
            self.testInput(self.input)
        elif not self.patternPlayed and self.completedPattern:
            self.playPattern()

    def testInput(self,input):

        if self.inputIdx >= len(self.pattern):
            self.completedPattern = True
            self.pattern.append(random.randint(0,3))
            self.patternPlayed = False
            self.inputIdx = 0
            self.score += 1

        if not self.completedPattern:
            if self.input == A_EVENT and self.pattern[self.inputIdx] == 0:
                self.topLeftRect.fill = 0xF8FF00
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 262, duration=0.3)
                time.sleep(.3)
                self.topLeftRect.fill = 0xFEFFD1
                self.inputIdx += 1
            elif self.input == C_EVENT and self.pattern[self.inputIdx] == 1:
                self.topRightRect.fill = 0x002FFF
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 294, duration=0.3)
                time.sleep(.3)
                self.topRightRect.fill = 0xAEBDFF
                self.inputIdx += 1
            elif self.input == B_EVENT and self.pattern[self.inputIdx] == 2:
                self.botLeftRect.fill = 0xFF0000
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 330, duration=0.3)
                time.sleep(.3)
                self.botLeftRect.fill = 0xFFA1A1
                self.inputIdx += 1
            elif self.input == D_EVENT and self.pattern[self.inputIdx] == 3:
                self.botRightRect.fill = 0x00FF36
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 392, duration=0.3)
                time.sleep(.3)
                self.botRightRect.fill = 0xB4FFC4
                self.inputIdx += 1
            elif self.input == A_EVENT or self.input == B_EVENT or self.input == C_EVENT or self.input == D_EVENT:
                self.gameOver = True


    def playPattern(self):

        for color in self.pattern:
            if color == 0:
                self.topLeftRect.fill = 0xF8FF00
                self.monster.monSprite.x = self.topLeftRect.x + (60 - int(self.monster.resolution/2))
                self.monster.monSprite.y = self.topLeftRect.y + (34 - int(self.monster.resolution/2))
                self.monster.monSprite.flip_x = True
                self.monster.monSprite[0] = 6
                time.sleep(.25)
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 262, duration=0.3)
                time.sleep(.3)
                self.monster.monSprite[0] = 6
                self.topLeftRect.fill = 0xFEFFD1
            elif color == 1:
                self.topRightRect.fill = 0x002FFF
                self.monster.monSprite.x = self.topRightRect.x + (60 - int(self.monster.resolution/2))
                self.monster.monSprite.y = self.topRightRect.y + (34 - int(self.monster.resolution/2))
                self.monster.monSprite.flip_x = False
                self.monster.monSprite[0] = 6
                time.sleep(.25)
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 294, duration=0.3)
                time.sleep(.3)
                self.monster.monSprite[0] = 6
                self.topRightRect.fill = 0xAEBDFF
            elif color == 2:
                self.botLeftRect.fill = 0xFF0000
                self.monster.monSprite.x = self.botLeftRect.x + (60 - int(self.monster.resolution/2))
                self.monster.monSprite.y = self.botLeftRect.y + (34 - int(self.monster.resolution/2))
                self.monster.monSprite.flip_x = True
                self.monster.monSprite[0] = 6
                time.sleep(.25)
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 330, duration=0.3)
                time.sleep(.3)
                self.monster.monSprite[0] = 6
                self.botLeftRect.fill = 0xFFA1A1
            elif color == 3:
                self.botRightRect.fill = 0x00FF36
                self.monster.monSprite.x = self.botRightRect.x + (60 - int(self.monster.resolution/2))
                self.monster.monSprite.y = self.botRightRect.y + (34 - int(self.monster.resolution/2))
                self.monster.monSprite.flip_x = False
                self.monster.monSprite[0] = 6
                time.sleep(.25)
                self.monster.monSprite[0] = 5
                simpleio.tone(board.GP9, 392, duration=0.3)
                time.sleep(.3)
                self.monster.monSprite[0] = 6
                self.botRightRect.fill = 0xB4FFC4
            time.sleep(.1)
        self.monster.monSprite.x = 120 - int(self.monster.resolution/2)
        self.monster.monSprite.y = 68 - int(self.monster.resolution/2)
        self.patternPlayed = True
        self.completedPattern = False
        self.inputCtrl.timeSinceInput = time.monotonic()
        self.inputCtrl.keys.events.clear()
        self.input = None

    def destroy(self):
        try:
            self.gameGroup.remove(self.monster.monSprite)
        except ValueError:
            pass

class SpdGameScreen(Screen):

    def __init__(self, monster, inputCtrl):
        super().__init__(monster, inputCtrl)

        self.holeSheet, self.holePalette = adafruit_imageload.load(
            "/sprites/games/spd/hole.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.holeSprite = displayio.TileGrid(
            self.holeSheet, pixel_shader=self.holePalette, width=1, height=1, tile_width=16, tile_height=16
        )
        self.targetSheet, self.targetPalette = adafruit_imageload.load(
            "/sprites/games/spd/target.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.targetSprite = displayio.TileGrid(
            self.targetSheet, pixel_shader=self.targetPalette, width=1, height=1, tile_width=16, tile_height=16
        )

        self.holePalette.make_transparent(0)
        self.targetPalette.make_transparent(0)

        self.enemyScale = displayio.Group(scale=3)
        self.enemyScale.append(self.holeSprite)

        self.enemies = displayio.Group(scale=1)
        self.enemies.append(self.enemyScale)

        self.enemyScale.x = 200
        self.enemyScale.y = 56

        self.showRules = True
        self.rules1 = label.Label(terminalio.FONT, text="Jump to avoid", color=0xFF0F00)
        self.rules2 = label.Label(terminalio.FONT, text="The Obstacles", color=0xFF0F00)

        self.rules1.y = 15
        self.rules2.y = 35
        self.rules2.x = 8

        self.rulesGroup = displayio.Group(scale=2)
        self.rulesGroup.append(self.rules1)
        self.rulesGroup.append(self.rules2)

        self.street = Rect(0,50,240,68,fill=0x706f6d)
        self.bottom = Rect(0,118,240,15,fill=0x262525)

        self.marks = displayio.Group(scale=1)
        for x in range(12):
            self.marks.append(Rect(x*24,84,15,3,fill=0xb0f00e))

        self.rail1 = Rect(0,40,240,4,fill=0x4f4e4d)
        self.rail2 = Rect(0,108,240,4,fill=0x4f4e4d)

        self.topRails = displayio.Group(scale=1)
        for x in range(26):
            self.topRails.append(Rect(x*10,40,5,10,fill=0x403e3d))

        self.botRails = displayio.Group(scale=1)
        for x in range(26):
            self.botRails.append(Rect(x*10,108,5,10,fill=0x403e3d))

        self.monster.monSprite.x = 10
        self.monster.monSprite.y = 70 - int(self.monster.resolution/2)

        self.bgGroup = displayio.Group(scale=2)
        self.bgGroup.append(self.monster.idleBgSprite)

        self.btnLabel1 = label.Label(terminalio.FONT, text="Jump", color=0x000000)
        self.btnLabel2 = label.Label(terminalio.FONT, text="Attack", color=0x000000)
        self.btnLabel3 = label.Label(terminalio.FONT, text="Defend", color=0x000000)

        self.btnLabel1.x = 2
        self.btnLabel1.y = 4
        self.btnLabel2.x = 82
        self.btnLabel2.y = 4
        self.btnLabel3.x = 82
        self.btnLabel3.y = 62

        self.buttonGroup = displayio.Group(scale=2)
        self.buttonGroup.append(self.btnLabel1)
        self.buttonGroup.append(self.btnLabel2)
        self.buttonGroup.append(self.btnLabel3)

        self.gameGroup = displayio.Group(scale=1)

        self.gameGroup.append(self.bgGroup)
        self.gameGroup.append(self.street)
        self.gameGroup.append(self.bottom)
        self.gameGroup.append(self.rail1)
        self.gameGroup.append(self.topRails)
        self.gameGroup.append(self.marks)
        self.gameGroup.append(self.enemies)
        self.gameGroup.append(self.monster.monSprite)
        self.gameGroup.append(self.botRails)
        self.gameGroup.append(self.rail2)
        self.gameGroup.append(self.buttonGroup)

        self.main.append(self.rulesGroup)

        self.gameOver = False
        self.score = 1

        self.moveTime = time.monotonic()
        self.animSpeed = .33
        self.speed = 5
        self.jumping = False
        self.defending = False
        self.attacking = False
        self.enemyAdded = time.monotonic()

    def update(self):
        #print(gc.mem_free())
        if not self.gameOver:
            self.handleInput()
        else:
            self.endGame()

        if not self.showRules:
            if not self.jumping and not self.attacking and not self.defending:
                self.charAnimator.walkInPlace(False,self.animSpeed)
            elif self.jumping:
                if not self.charAnimator.jump(False,self.animSpeed):
                    self.jumping = False
            elif self.defending:
                pass
            elif self.attacking:
                pass
            self.moveElements()
            self.checkCollisions()
            if (self.enemyAdded + 50/self.speed) < time.monotonic():
                self.addEnemy()
                self.enemyAdded = time.monotonic()
            self.speed = 5 + self.score
            self.animSpeed = .33 / self.score

    def addEnemy(self):
        enemyToAdd = random.randint(0,1)
        print(enemyToAdd)
        if enemyToAdd == 0:
            newEnemyScale = displayio.Group(scale=3)
            newEnemySprite = displayio.TileGrid(
                self.holeSheet, pixel_shader=self.holePalette, width=1, height=1, tile_width=16, tile_height=16
            )
            newEnemyScale.append(newEnemySprite)
            newEnemyScale.y = 56
            newEnemyScale.x = 240 + random.randint(0,60)
            self.enemies.append(newEnemyScale)
        elif enemyToAdd == 1:
            newEnemyScale = displayio.Group(scale=4)
            newEnemySprite = displayio.TileGrid(
                self.targetSheet, pixel_shader=self.targetPalette, width=1, height=1, tile_width=16, tile_height=16
            )
            newEnemyScale.append(newEnemySprite)
            newEnemyScale.y = 40
            newEnemyScale.x = 240 + random.randint(0,60)
            self.enemies.append(newEnemyScale)
        else:
            pass

    def moveElements(self):
        if (self.moveTime + self.animSpeed) < time.monotonic():
            for mark in self.marks:
                if mark.x <= -24:
                    mark.x += 264 - (3 + self.speed)
                else:
                    mark.x -= 3 + self.speed
            for rail in self.topRails:
                if rail.x <= -10:
                    rail.x += 250 - (3 + self.speed)
                else:
                    rail.x -= 3 + self.speed
            for rail in self.botRails:
                if rail.x <= -10:
                    rail.x += 250 - (3 + self.speed)
                else:
                    rail.x -= 3 + self.speed
            for enemy in self.enemies:
                if enemy.x <= -64:
                    self.enemies.remove(enemy)
                    self.score += 1
                else:
                    enemy.x -= 3 + self.speed


            self.moveTime = time.monotonic()

    def checkCollisions(self):
        for enemy in self.enemies:
            if enemy.x < self.monster.monSprite.x + self.monster.resolution - 15 and enemy.x > self.monster.monSprite.x and not self.jumping:
                self.gameOver = True

    def endGame(self):

        self.gameGroup.remove(self.monster.monSprite)
        endText1 = label.Label(terminalio.FONT, text="Game Over!", color=0xFF0F00)
        endText2 = label.Label(terminalio.FONT, text="Score: " + str(self.score), color=0xFF0F00)
        endText1.y = 15
        endText2.y = 35
        self.rulesGroup.remove(self.rules1)
        self.rulesGroup.remove(self.rules2)
        self.rulesGroup.append(endText1)
        self.rulesGroup.append(endText2)
        self.main.remove(self.gameGroup)
        self.main.append(self.rulesGroup)
        time.sleep(4)
        self.transition = "idle"

    def handleInput(self):

        self.input = self.inputCtrl.getInput()
        if self.input != None:
            self.inputCtrl.timeSinceInput = time.monotonic()

        if self.input:
            if self.input == A_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                else:
                    self.jumping = True

            elif self.input == B_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                else:
                    pass
            elif self.input == D_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                else:
                    self.attacking = True
            elif self.input == C_EVENT:
                if self.showRules:
                    self.showRules = False
                    self.main.remove(self.rulesGroup)
                    self.main.append(self.gameGroup)
                else:
                    self.defending = True

    def destroy(self):
        try:
            self.gameGroup.remove(self.monster.monSprite)
        except ValueError:
            pass
        try:
            self.bgGroup.remove(self.monster.idleBgSprite)
        except ValueError:
            pass