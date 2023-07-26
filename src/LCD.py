import Adafruit_CharLCD as LCDC
import time
from time import sleep
#from gpiozero import DistanceSensor

class LCDController:
    def __init__(self):
        # Define LCD pin connections
        self.lcd_rs = 22  # Raspberry Pi GPIO pin connected to LCD RS
        self.lcd_en = 17  # Raspberry Pi GPIO pin connected to LCD EN
        self.lcd_d4 = 25  # Raspberry Pi GPIO pin connected to LCD D4
        self.lcd_d5 = 24  # Raspberry Pi GPIO pin connected to LCD D5
        self.lcd_d6 = 23  # Raspberry Pi GPIO pin connected to LCD D6
        self.lcd_d7 = 18  # Raspberry Pi GPIO pin connected to LCD D7

        # Define LCD column and row size
        self.lcd_columns = 16
        self.lcd_rows = 2

        # Initialize the LCD module
        self.lcd = LCDC.Adafruit_CharLCD(
            self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
            self.lcd_columns, self.lcd_rows
        )

    def clear_screen(self):
        self.lcd.clear()

    def display_text(self, text):
        self.lcd.message(text)

    def cursor(self, col, row):
        self.lcd.set_cursor(col, row)


