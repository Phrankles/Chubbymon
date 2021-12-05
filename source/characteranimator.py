# Character Animator
import time
import random
import adafruit_imageload
import displayio

class CharacterAnimator:

    def __init__(self,monSprite,monster):

        self.monSprite = monSprite

        self.monster = monster

        self.animIndex = 0
        self.animTime = time.monotonic()

        self.direction = 0
        self.distance = 0

        self.animLayer = displayio.Group(scale=1)

    def walkUpRight(self):

        self.monSprite.flip_x = True
        if self.monSprite.y >= 65:
            self.monSprite.y -= 3
        if self.monSprite.x <= 220:
            self.monSprite.x += 3
        if self.monSprite[0] != 8:
            self.monSprite[0] = 8
        else:
            self.monSprite[0] = 9
        self.animTime = time.monotonic()
        self.distance -= 1

    def walkUpLeft(self):

        self.monSprite.flip_x = False
        if self.monSprite.y >= 65:
            self.monSprite.y -= 3
        if self.monSprite.x >= -10:
            self.monSprite.x -= 3
        if self.monSprite[0] != 8:
            self.monSprite[0] = 8
        else:
            self.monSprite[0] = 9
        self.animTime = time.monotonic()
        self.distance -= 1

    def walkDownRight(self):

        self.monSprite.flip_x = True
        if self.monSprite.y <= 110:
            self.monSprite.y += 3
        if self.monSprite.x <= 220:
            self.monSprite.x += 3
        if self.monSprite[0] != 0:
            self.monSprite[0] = 0
        else:
            self.monSprite[0] = 1
        self.animTime = time.monotonic()

    def walkDownLeft(self):

        self.monSprite.flip_x = False
        if self.monSprite.y <= 110:
            self.monSprite.y += 3
        if self.monSprite.x >= -10:
            self.monSprite.x -= 3
        if self.monSprite[0] != 0:
            self.monSprite[0] = 0
        else:
            self.monSprite[0] = 1

        self.animTime = time.monotonic()

    def idleInPlace(self):

        if random.randint(1,8) == 1:
            self.monSprite.flip_x = True
        else:
            self.monSprite.flip_x = False
        if self.monster.isHappy():
            if self.monSprite[0] != 7:
                self.monSprite[0] = 7
            else:
                self.monSprite[0] = 6
        elif self.monster.isContent():
            if self.monSprite[0] != 4:
                self.monSprite[0] = 4
            else:
                self.monSprite[0] = 6
        elif self.monster.isMad():
            if self.monSprite[0] != 3:
                self.monSprite[0] = 3
            else:
                self.monSprite[0] = 6

        
        self.animTime = time.monotonic()

    def randomIdle(self):
        #Generate random movement
        if self.distance <= 0:
            self.direction = random.randint(1,10)
            self.distance = random.randint(2,10)

        if (self.animTime + .33) < time.monotonic():
            #Up Right
            if self.direction == 1 or self.direction == 2:
                self.walkUpRight()
                self.distance -= 1

            #Down Left
            elif self.direction == 3 or self.direction == 4:
                self.walkDownLeft()
                self.distance -= 1

            #Up Left
            elif self.direction == 5 or self.direction == 6:
                self.walkUpLeft()
                self.distance -= 1

            #Down Right
            elif self.direction == 7 or self.direction == 8:
                self.walkDownRight()
                self.distance -= 1

            #Idle
            else:
                if self.distance > 4:
                    self.distance = 4
                self.idleInPlace()
                self.distance -= 1

            if self.animIndex > 2:
                self.animIndex = 0

    def simpleIdle(self):
        #simple 2 frame idle animation (bg characters)
        if (self.animTime + .33) < time.monotonic():            
            if self.monster.isHappy():
                if self.monSprite[0] != 7:
                    self.monSprite[0] = 7
                else:
                    self.monSprite[0] = 6
            elif self.monster.isContent():
                if self.monSprite[0] != 4:
                    self.monSprite[0] = 4
                else:
                    self.monSprite[0] = 6
            elif self.monster.isMad():
                if self.monSprite[0] != 3:
                    self.monSprite[0] = 3
                else:
                    self.monSprite[0] = 6
            self.animTime = time.monotonic()

    def feedMeat(self):
        meatSheet, meatPalette = adafruit_imageload.load(
            "/sprites/animations/eat_meat.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        meatPalette.make_transparent(0)
        meatSprite = displayio.TileGrid(
            meatSheet, pixel_shader=meatPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        meatSprite.x = self.monSprite.x
        meatSprite.y = self.monSprite.y

        if self.monSprite.flip_x:
            meatSprite.flip_x = True
            meatSprite.x += 20
        else:
            meatSprite.x -= 20

        self.animLayer.append(meatSprite)
        meatSprite[0] = 0
        self.monSprite[0] = 1
        time.sleep(.5)
        self.monSprite[0] = 5
        time.sleep(.5)
        meatSprite[0] = 1
        self.monSprite[0] = 1
        time.sleep(.5)
        self.monSprite[0] = 5
        time.sleep(.5)        
        meatSprite[0] = 2
        self.monSprite[0] = 1
        time.sleep(.5)        
        self.monSprite[0] = 5
        time.sleep(.5)
        self.monSprite[0] = 1
        self.animLayer.pop()
        time.sleep(.5)

    def feedProtien(self):

        meatSheet, meatPalette = adafruit_imageload.load(
            "/sprites/animations/eat_meat.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        meatPalette.make_transparent(0)
        meatSprite = displayio.TileGrid(
            meatSheet, pixel_shader=meatPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        meatSprite.x = self.monSprite.x
        meatSprite.y = self.monSprite.y

        if self.monSprite.flip_x:
            meatSprite.flip_x = True
            meatSprite.x += 20
        else:
            meatSprite.x -= 20

        self.animLayer.append(meatSprite)
        meatSprite[0] = 0
        self.monSprite[0] = 1
        time.sleep(.5)
        self.monSprite[0] = 5
        time.sleep(.5)
        meatSprite[0] = 1
        self.monSprite[0] = 1
        time.sleep(.5)
        self.monSprite[0] = 5
        time.sleep(.5)        
        meatSprite[0] = 2
        self.monSprite[0] = 1
        time.sleep(.5)        
        self.monSprite[0] = 5
        time.sleep(.5)
        self.monSprite[0] = 1
        self.animLayer.pop()
        time.sleep(.5)

    def poop(self):
        pass
