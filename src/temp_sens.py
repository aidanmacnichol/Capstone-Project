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


#       """
#       Sensor has 8 pixels. Each pixels temperature value is represented with two bytes.
#       That gives us 16 bytes then there are two bytes for the PTAT + one for the checksum:

#       [  0  |   1  | 2  | 3  .....  16 |  17 |  18 ]                        
#       [ptat | ptat | t1 | t2 ..... t15 | t16 | CRC ]

#       To calculate a temperature value for a pixel we take first byte + second byte * 256 *0.1

#       """


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




#************************************* THIS ONE SUCKS ****************************************************

# i2c_bus = smbus.SMBus(1)
# OMRON_1=0x0a 					# 7 bit I2C address of Omron MEMS Temp Sensor D6T-44L **
# OMRON_BUFFER_LENGTH=35				# Omron data buffer size **
# temperature_data=[0]*OMRON_BUFFER_LENGTH 	# initialize the temperature data list **

# # intialize the pigpio library and socket connection to the daemon (pigpiod)
# pi = pigpio.pi()              # use defaults ** 
# version = pi.get_pigpio_version() **
# print('PiGPIO version = '+str(version)) **
# handle = pi.i2c_open(1, 0x0a) # open Omron D6T device at address 0x0a on bus 1 **

# # initialize the device based on Omron's appnote 1
# result=i2c_bus.write_byte(OMRON_1,0x4c); ** 
# #print 'write result = '+str(result)

# #for x in range(0, len(temperature_data)):
#    #print x
#    # Read all data  tem
#    #temperature_data[x]=i2c_bus.read_byte(OMRON_1)
# (bytes_read, temperature_data) = pi.i2c_read_device(handle, len(temperature_data))

# temperature=[0]*OMRON_BUFFER_LENGTH
# a = 0

# for i in range(2, len(temperature_data)-2, 2):
#    temperature[a] = float((temperature_data[i+1] << 8) | temperature_data[i])/10
#    a += 1

# # Display data 
# print('Bytes read from Omron D6T: '+str(bytes_read))
# print('Data read from Omron D6T : ')
# # for x in range(bytes_read):
# #    print(temperature_data[x]),

# print(temperature)
# #print 'done'