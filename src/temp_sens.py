import smbus
import sys
import getopt
import time 
import pigpio
import crcmod.predefined

"""
      The sensor has one pixel LMFAO

      [     0    |     1     |     2     |     3     |     4      ]
      [ PTAT Lo  | PTAT Hi   |   P0 Lo   |   P0 Hi   |   PEC      ]

      SDA: (temp blue) pin 3      --THESE PINS ARE I2c channel 1
      SCL: (temp yellow) pin 5
      rn have a 10k pullup resistor


      To calculate a temperature value for a pixel we take first byte + second byte * 256 *0.1

"""


class temp_sens:
   pi = pigpio.pi()



   def __init__(self, address=0x0a):

     # self.CRC = 0xa4/(16/1)
      try:
         self.handle = self.pi.i2c_open(1, 0x0a)
      except AttributeError:
         print('run "sudo pigpiod" idiot')
         raise
   
   def D6T_checkPEC(buf, pPEC):
      crc = calc_crc(0x14)
      crc = calc_crc(0x4C ^ crc)
      crc = calc_crc(0x15 ^ crc)

      i = 0

      while i < pPEC:
         crc = calc_crc(readbuff[i] ^ crc)
         i += 1
      
      return (crc == readbuff[pPEC])
   
   def readData(self):
      self.pi.i2c_write_device(self.handle, [0x4c])
      
      # Data is a tupule with first item being size of byte array (19 heres)
      data = self.pi.i2c_read_device(self.handle, 19) #19


      print(data)
      print(data[0])


      self.temp = []

      self.ptat = (data[1][1] *256 + data[1][0]) / 10

      #temp.append((data[1][3] * 256 + data[1][2]) / 10)

      
      self.temp.append((data[1][3] * 256 + data[1][2]) / 16.0)
      self.temp.append((data[1][5] * 256 + data[1][4]) / 10.0)
      self.temp.append((data[1][7] * 256 + data[1][6]) / 10.0)
      self.temp.append((data[1][9] * 256 + data[1][8]) / 10.0)
      self.temp.append((data[1][11] * 256 + data[1][10]) / 10.0)
      self.temp.append((data[1][13] * 256 + data[1][12]) / 10.0)
      self.temp.append((data[1][15] * 256 + data[1][14]) / 10.0)
      self.temp.append((data[1][17] * 256 + data[1][16]) / 10.0)

      self.crc8_function = crcmod.predefined.mkCrcFun('crc-8')

      # if self.crc8_function != self.CRC:
      #    print("CRC Error")

   #    if not self.D6T_checkPEC(data, 4):
   #       print("CRC error")

      return self.temp, self.ptat

   
   # def calc_crc(data):
   #    index = 0
   #    temp

   #    for i in range(8):
   #       temp = data
   #       data <<= 1
   #       if temp & 0x80:
   #          data ^= 0x07
   #    return data
   
      


if __name__ == '__main__':
   sensor = temp_sens()

   while(True):
      temp, ptat = sensor.readData()
      print(temp)
      print(f"ptat: {ptat}")
      time.sleep(1)

