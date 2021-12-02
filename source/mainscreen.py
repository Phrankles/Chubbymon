class MainScreen:

    def __init__(self,monster,display):

        self.monster = monster
        self.name = self.monster.name

        self.display = display

        self.selectIdx = 0
        self.displaySelect = True
        self.lockSelIdx = False

        self.menuIdx = 0

        #Menu BG Sprite load
        self.menuBgSheet,self.menuBgPalette = adafruit_imageload.load(
            "/sprites/menu_bg.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        self.menuSelectSprite = displayio.TileGrid(
            self.selectSheet, pixel_shader=self.selectPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        self.menuBgSprite = displayio.TileGrid(
            self.menuBgSheet, pixel_shader=self.menuBgPalette, width=1, height=1, tile_width=60, tile_height=34
        )
        self.menuBgSprite.flip_y = True

        self.menuBgGroup = displayio.Group(scale=4)
        self.menuGroup = displayio.Group(scale=1)


    def displayMain(self):
        if self.selectIdx == 0 and self.displaySelect:
            self.main.remove(self.selectGroup)
            self.main.remove(self.iconGroup)
            try:
                self.main.remove(self.menuGroup)
            except ValueError:
                pass
            self.displaySelect = False
        elif self.selectIdx > 0 and not self.displaySelect:
            self.main.append(self.iconGroup)
            self.main.insert(self.main.index(self.iconGroup),self.selectGroup)
            self.displaySelect = True

        self.display.show(self.main)
        self.randomMovement()
        self.updateSelPos()



    def initMenu(self):
        self.menuIdx = 0
        for x in self.menuGroup:
            self.menuGroup.remove(x)
        try:
            self.menuGroup.append(self.menuBgGroup)
        except ValueError:
            pass
        try:
            self.main.append(self.menuGroup)
        except ValueError:
            pass

    def updateMenuStatus(self):
        pass

    def updateMenuFeed(self):

        if self.menuIdx < 1:
            self.menuIdx += 1
        else:
            self.menuIdx = 0

        if self.menuIdx == 0:
            print("executed")
            try:
                self.menuGroup[1][0].x =20
                self.menuGroup[1][0].y =18

            except ValueError:
                print("failed")
                pass

        else:
            try:
                self.menuSelectSprite.x =70
                self.menuSelectSprite.y =18
            except ValueError:
                print("failed")
                pass

    def updateMenuTrain(self):
        pass

    def updateMenuBattle(self):
        pass

    def updateMenuLights(self):
        pass

    def updateMenuMedicine(self):
        pass

    def updateMenuJournal(self):
        pass

    def updateMenuLink(self):
        pass

    def showMenu(self):
        if self.selectIdx != 0:
            self.lockSelIdx = True
            if self.selectIdx == 1:
                self.showMenuStatus()
            if self.selectIdx == 2:
                self.showMenuFeed()
            if self.selectIdx == 3:
                self.showMenuTrain()
            if self.selectIdx == 4:
                self.showMenuBattle()
            if self.selectIdx == 5:
                self.cleanPoop()
            if self.selectIdx == 6:
                self.showMenuLights()
            if self.selectIdx == 7:
                self.showMenuMedicine()
            if self.selectIdx == 8:
                self.showMenuJournal()
            if self.selectIdx == 9:
                self.showMenuLink()

    def showMenuStatus(self):
        self.initMenu()

        nameArea = label.Label(terminalio.FONT, text="Name: " + self.monster.name, color=0xCE3312)
        nameArea.x = 10
        nameArea.y =10

        ageArea = label.Label(terminalio.FONT, text="Age: " + str(int(self.monster.age/86400)) + "y", color=0xCE3312)
        ageArea.x = 10
        ageArea.y =20

        weightArea = label.Label(terminalio.FONT, text="Weight: " + str(self.monster.weight), color=0xCE3312)
        weightArea.x = 60
        weightArea.y =20

        hungerArea = label.Label(terminalio.FONT, text="Hunger: " + str(self.monster.hunger), color=0xCE3312)
        hungerArea.x = 10
        hungerArea.y =30

        strengthArea = label.Label(terminalio.FONT, text="Strength: " + str(self.monster.strength), color=0xCE3312)
        strengthArea.x = 10
        strengthArea.y =40

        effortArea = label.Label(terminalio.FONT, text="Effort: " + str(self.monster.effort), color=0xCE3312)
        effortArea.x = 10
        effortArea.y =50

        menuMon = displayio.TileGrid(
            self.charSheet, pixel_shader=self.charPalette, width=1, height=1, tile_width=32, tile_height=32
        )

        menuMon.x = 85
        menuMon.y = 27

        statsGroup = displayio.Group(scale=2)
        statsGroup.append(nameArea)
        statsGroup.append(ageArea)
        statsGroup.append(weightArea)
        statsGroup.append(hungerArea)
        statsGroup.append(strengthArea)
        statsGroup.append(effortArea)
        statsGroup.append(menuMon)
        try:
            self.menuGroup.append(statsGroup)
        except ValueError:
            pass


    def showMenuFeed(self):
        self.initMenu()


        icnSheet, icnPalette = adafruit_imageload.load(
            "/sprites/select.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        icnPalette.make_transparent(0)
        icnPalette.make_transparent(1)
        icnPalette.make_transparent(2)
        icnPalette.make_transparent(3)
        icnIcon = displayio.TileGrid(
            icnSheet, pixel_shader=icnPalette, width=1, height=1, tile_width=32, tile_height=32
        )


        meatSheet, meatPalette = adafruit_imageload.load(
            "/sprites/meat.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        meatPalette.make_transparent(0)
        meatIcon = displayio.TileGrid(
            meatSheet, pixel_shader=meatPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        meatIcon.x = 20
        meatIcon.y = 18

        protienSheet, protienPalette = adafruit_imageload.load(
            "/sprites/protien.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        protienPalette.make_transparent(0)
        protienIcon = displayio.TileGrid(
            protienSheet, pixel_shader=protienPalette, width=1, height=1, tile_width=32, tile_height=32
        )
        protienIcon.x = 70
        protienIcon.y = 18

        self.menuSelectSprite.x = meatIcon.x
        self.menuSelectSprite.y = meatIcon.y

        foodGroup = displayio.Group(scale=2)
        try:
            foodGroup.append(self.menuSelectSprite)
            foodGroup.append(meatIcon)
            foodGroup.append(protienIcon)
        except ValueError:
            pass

        self.menuGroup.append(foodGroup)

        self.monster.feedMeat()

    def showMenuTrain(self):
        self.initMenu()

    def showMenuBattle(self):
        self.initMenu()

    def cleanPoop(self):

        self.monster.cleanPoop()
        self.lockSelIdx = False

    def showMenuLights(self):
        self.initMenu()

    def showMenuMedicine(self):
        self.initMenu()

    def showMenuJournal(self):
        self.initMenu()

    def showMenuLink(self):
        self.initMenu()

    def manageInput(self,input):
        if input == "B":
            if not self.lockSelIdx:
                if self.selectIdx < 9:
                    self.selectIdx += 1
                else:
                    self.selectIdx = 1
            else:
                self.updateMenuPos()
        elif input == "A":
            self.selectIdx = 0
            self.lockSelIdx = False
        elif input == "C":
            if not self.lockSelIdx:
                self.showMenu()
        elif input == "D":
            pass
        elif input == "icon-timeout":
            self.selectIdx = 0
            self.menuIdx = 0
            self.lockSelIdx = False



