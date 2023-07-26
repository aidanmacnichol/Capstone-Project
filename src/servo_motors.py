import RPi.GPIO as GPIO
import time
from RaspberryMotors.motors import servos
import pigpio

#Class for moving servo motors
class servo_motors:
    xservo = 11 #p in # of xservo
    yservo = 5 #pin # of y servo 
    centerx = 160
    centery = 120
    duty_x = 1500
    duty_y = 1900
    pwm = pigpio.pi()

    
    duty = 12
    
    box_size = 20 #range of coordinates it tries to center within
    
    def __init__(self):
        
        # Center servos upon start
        self.pwm.set_mode(self.xservo, pigpio.OUTPUT)
        self.pwm.set_mode(self.yservo, pigpio.OUTPUT)
        
        self.pwm.set_PWM_frequency(self.xservo, 50)
        self.pwm.set_PWM_frequency(self.yservo, 50)
        
        self.pwm.set_servo_pulsewidth(self.xservo, self.duty_x)
        self.pwm.set_servo_pulsewidth(self.yservo, self.duty_y)
        
    
    # Cleanup PWM pins
    def cleanup(self):
        self.pwm.set_PWM_dutycycle(self.xservo, 0 )
        self.pwm.set_PWM_frequency(self.yservo, 0 )
    

    def moveServos(self, cord):
        # Calculate difference between the center of frame and current coordinates
        x_diff = cord[0] - self.centerx
        y_diff = cord[1] - self.centery

        # Check if we are outside margin of error on x plane
        if abs(x_diff) > self.box_size:
            # move left or right depending on servo location and forehead coordinates
            # also check we are not outside range of servos
            if x_diff > 0:
                self.duty_x -= self.duty
                if self.duty_x < 500:
                    self.duty_x = 500
            elif x_diff < self.box_size:
                self.duty_x += self.duty
                if self.duty_x > 2500:
                    self.duty_x = 2500

        # Check if we are outside margin of error on y plane
        if abs(y_diff) > self.box_size:
            # move up or down depending on servo location and forehead coordinates
            # also check we are not outside range of servos
            if y_diff > 0:
                self.duty_y -= self.duty
                if self.duty_y < 500:
                    self.duty_y = 500
            elif y_diff < 0:
                self.duty_y += self.duty
                if self.duty_y > 2500:
                    self.duty_y = 2500
            else:
                return
        
        # Move servos to new coordinates
        self.pwm.set_mode(self.xservo, pigpio.OUTPUT)
        self.pwm.set_mode(self.yservo, pigpio.OUTPUT)
        
        self.pwm.set_PWM_frequency(self.xservo, 50)
        self.pwm.set_PWM_frequency(self.yservo, 50)
        
        self.pwm.set_servo_pulsewidth(self.xservo, self.duty_x)
        self.pwm.set_servo_pulsewidth(self.yservo, self.duty_y)
            

if __name__ == '__main__':
    xMotor = servo_motors()
    xMotor.cleanup()


