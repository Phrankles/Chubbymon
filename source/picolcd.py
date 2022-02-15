# File to initialize the WaveShare PicoLCD
# and return the Circuit Python ST7789 object
import board
import displayio
import busio
import time
from adafruit_display_text import label
from adafruit_st7789 import ST7789

class PicoLCD:

    def __init__(self):
        displayio.release_displays()
        self.spi = busio.SPI(clock=board.GP18,MOSI=board.GP19)
        self.tft_cs = board.GP17
        self.tft_dc = board.GP16
        #self.tft_reset = board.RUN
        self.display_bus = displayio.FourWire(self.spi, command=self.tft_dc, chip_select=self.tft_cs)
        self.display = ST7789(
            self.display_bus, rotation=90, width=240, height=135, rowstart=40, colstart=53, backlight_pin = board.GP20
        )

    def returnLCD(self):
        return self.display

    def releaseLCD(self):
        self.display.brightness = 0
        
        
    def reinitLCD(self):
        self.display.brightness = 1