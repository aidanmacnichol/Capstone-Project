import smbus
import sys
import getopt
import time 
import pigpio

"""
      The sensor has eight pixels

      [     0    |     1     |     2     |     3     | ...OTHER TEMP PIXELS... |     18     ]
      [ PTAT Lo  | PTAT Hi   |   P0 Lo   |   P0 Hi   | ...OTHER TEMP PIXELS... |   PEC      ]

      SDA: (temp blue) pin 3      --THESE PINS ARE I2c channel 1
      SCL: (temp yellow) pin 5
      rn have a 10k pullup resistor
      To calculate a temperature value for a pixel we take first byte + second byte * 256 / divisor

"""

class temp_sens:
   pi = pigpio.pi()
   divisor = 15.6


   def __init__(self, address=0x0a):
      # open i2c connection 
      try:
         self.handle = self.pi.i2c_open(1, 0x0a)
      except AttributeError:
         print('run "sudo pigpiod" please')
         raise
   
   
   def readData(self):
      self.pi.i2c_write_device(self.handle, [0x4c])
      
      # Data is a tupule with first item being size of byte array (19 heres)
      data = self.pi.i2c_read_device(self.handle, 19) #19

      # get temp data array
      self.temp = []
      
      # ptat value
      self.ptat = (data[1][1] *256 + data[1][0]) / self.divisor


      # Calculating the 8 temperature pixels
      self.temp.append((data[1][3] * 256 + data[1][2]) / self.divisor)
      self.temp.append((data[1][5] * 256 + data[1][4]) / self.divisor)
      self.temp.append((data[1][7] * 256 + data[1][6]) / self.divisor)
      self.temp.append((data[1][9] * 256 + data[1][8]) / self.divisor)
      self.temp.append((data[1][11] * 256 + data[1][10]) / self.divisor)
      self.temp.append((data[1][13] * 256 + data[1][12]) / self.divisor)
      self.temp.append((data[1][15] * 256 + data[1][14]) / self.divisor)
      self.temp.append((data[1][17] * 256 + data[1][16]) / self.divisor)

      return self.temp, self.ptat


if __name__ == '__main__':
   sensor = temp_sens()

   while(True):
      temp, ptat = sensor.readData()
      print(temp)
      print(f"ptat: {ptat}")
      time.sleep(1)


