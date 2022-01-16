import threading

# import RPi.GPIO as GPIO
import OPi.GPIO as GPIO

from RPLCD import CharLCD
import time
import sys

START_STOP_DELAY = 3
REFRESH_DELAY = 0.5

PIN_RESET = 5
PIN_RW = 3
PIN_ENABLE = 7
PIN_DATA = [12, 11, 8, 10]

# Do not change unless you want to change the update routine as well 
LCD_COLUMNS = 16
LCD_ROWS = 2
LCD_DOTSIZE = 8

class LCDManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.upperLine = ["  Initializing  "]
        self.lowerLine = [""]
        self.offset = 0
        self.currentIndex = 0
        self.startStopTimer = time.time()

        self.lcd = CharLCD(pin_rs=PIN_RESET, pin_rw=PIN_RW, pin_e=PIN_ENABLE, pins_data=PIN_DATA,
              numbering_mode=GPIO.BOARD,
              cols=LCD_COLUMNS, rows=LCD_ROWS, dotsize=LCD_DOTSIZE,
              auto_linebreaks=True,
              pin_backlight=None, backlight_enabled=False)

        self.start()

    def calcRowText(self, scrollText, offset=0):
        if len(scrollText) < LCD_COLUMNS:
            for a in range(0, LCD_COLUMNS-len(scrollText)):
                scrollText += " "
        line = scrollText[offset:offset+LCD_COLUMNS]
        return line

    def setUpper(self, newUpper):
        self.upperLine = newUpper
        self.offset = 0
        self.currentIndex = 0


    def update(self):
        currentUpperLine = self.calcRowText(self.upperLine[self.currentIndex], self.offset)
        currentLowerLine = self.calcRowText(self.lowerLine[0])
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(currentUpperLine)
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(currentLowerLine)
        if time.time() - self.startStopTimer > START_STOP_DELAY:
            self.offset += 1
            if self.offset >= len(self.upperLine[self.currentIndex]) - (LCD_COLUMNS-1):
                self.offset = 0
            
            if self.offset == 0 or self.offset == len(self.upperLine[self.currentIndex]) - LCD_COLUMNS:
                self.startStopTimer = time.time()
                if self.offset == 0:
                    self.currentIndex += 1
                    if self.currentIndex == len(self.upperLine):
                        self.currentIndex = 0
                
    def run(self):
        while True:
            # TODO: Add refresh delay.
            self.update()
