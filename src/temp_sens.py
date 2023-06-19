import smbus
import sys
import getopt
import time 
import pigpio

# class temp_sens(object):
#    def __init__(self, rasPiChannel=1, sensorAddress=0x0a, arraySize=8):
#       self.BUFFER_LENGTH = 19#(arraySize * 2) + 3 #idk why we do this yet
#       self.arraySize = arraySize
#       self.sensorAddress = sensorAddress
#       self.pi = pigpio.pi()
#       self.piGPIOver = self.pi.get_pigpio_version()
#       self.i2cBus = smbus.SMBus(1)


       """
       Sensor has 8 pixels. Each pixels temperature value is represented with two bytes.
       That gives us 16 bytes then there are two bytes for the PTAT + one for the checksum:

       [  0  |   1  | 2  | 3  .....  16 |  17 |  18 ]                        
       [ptat | ptat | t1 | t2 ..... t15 | t16 | CRC ]

       To calculate a temperature value for a pixel we take first byte + second byte * 256 *0.1
      

       HARDWARE SETUP:  
      
      SDA: (temp blue) pin 3      --THESE PINS ARE I2c channel 1
      SCL: (temp yellow) pin 5

      rn have a 10k pullup resistor
       """


#       # Initialize piGPIO = pi

#       time.sleep(0.05)
#       self.handle = self.pi.i2c_open(rasPiChannel, sensorAddress)
#       print(self.handle)
#       self.result = self.i2cBus.write_byte(self.sensorAddress, 0x4c)
   
#    def read(self):
#       self.temperature_data_raw=[0]*self.BUFFER_LENGTH
#       self.temperature=[0.0]*self.arraySize
#       self.values=[0]*self.BUFFER_LENGTH

#       (self.bytes_read, self.temperature_data_raw) = self.pi.i2c_read_device(self.handle, self.BUFFER_LENGTH)
#       # add error handling here maybe?

#       if self.bytes_read != self.BUFFER_LENGTH:
#          print("Bad byte count")

#       print(f"Raw Temp data: {self.temperature_data_raw} ")

#       # Calculate temp values
#       a = 0
#       for i in range(2, len(self.temperature_data_raw)-2, 2):
#          self.temperature[a] = float((self.temperature_data_raw[i] + self.temperature_data_raw[i+1]))
#          a += 1
      
#       print(f"converted: {self.temperature}")



# if __name__ == '__main__':
#    sensor = temp_sens()

#    while(True):
#       time.sleep(1)
#       sensor.read()

#**********************************************************************************************************


class temp_sens:
   pi = pigpio.pi()


   def __init__(self, address=0x0a):
      try:
         self.handle = self.pi.i2c_open(1, 0x0a)
      except AttributeError:
         print('run "sudo pigpiod" idiot')
         raise
   
   def readData(self):
      self.pi.i2c_write_device(self.handle, [0x4c])
      data = self.pi.i2c_read_device(self.handle, 19)

      print(data)

      temp = []

      temp.append((data[1][3] * 256 + data[1][2]) / 10)
      temp.append((data[1][5] * 256 + data[1][4]) / 10)
      temp.append((data[1][7] * 256 + data[1][6]) / 10)
      temp.append((data[1][9] * 256 + data[1][8]) / 10)
      temp.append((data[1][11] * 256 + data[1][10]) / 10)
      temp.append((data[1][13] * 256 + data[1][12]) / 10)
      temp.append((data[1][15] * 256 + data[1][14]) / 10)
      temp.append((data[1][17] * 256 + data[1][16]) / 10)

      return temp

if __name__ == '__main__':
   sensor = temp_sens()

   while(True):
      temp = sensor.readData()
      print(temp)
      time.sleep(1)

