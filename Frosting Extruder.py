#FROSTING EXTRUDER RASPBERRY PI CODE
#Senior Design Group 4, Texas Tech University
#Members: Evan, Christian, Tessa, Mosope, Travis
#Code written by Travis W., April 9th 2022

#red LED is pin GPIO17
#green LED is pin GPIO18
#motor is pin GPIO27, GPIO 22, and GPIO5
#green button is pin GPIO23
#red button is pin GPIO24
#left microswitch is pin GPIO12 (compression)
#right microswitch is pin GPIO16 (retraction)

import RPi.GPIO as GPIO #importing python libraries
import time

#assigning pins to variable names
MotorPin1 = 27 #motor pins, 3 in total
MotorPin2 = 22 
MotorEnable = 5 
microPinComp = 12 #left microswitch for compression
microPinRet = 16 #right microswitch for retraction
BtnPinY = 25 #yellow button is footswitch stand-in
LEDRed = 17 #Red LED
LEDGreen = 18 #Green LED
BtnPinR = 24 #Red button

#define setup section for assigning input/output variables
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotorPin1, GPIO.OUT)
    GPIO.setup(MotorPin2, GPIO.OUT)
    GPIO.setup(MotorEnable, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(microPinComp, GPIO.IN)
    GPIO.setup(microPinRet, GPIO.IN)
    GPIO.setup(BtnPinY, GPIO.IN)
    GPIO.setup(LEDRed, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LEDGreen, GPIO.OUT, initial=GPIO.HIGH)

# define a motor function to spin the motor
def motor(direction):
    # clockwise
    if direction == 1:
        # set direction
        GPIO.output(MotorPin1, GPIO.HIGH)
        GPIO.output(MotorPin2, GPIO.LOW)
        # enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        print ("Clockwise")
    # counterclockwise
    if direction == -1:
        # set direction
        GPIO.output(MotorPin1, GPIO.LOW)
        GPIO.output(MotorPin2, GPIO.HIGH)
        # enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        print ("Counterclockwise")
    # stop
    if direction == 0:
        # disable the motor
        GPIO.output(MotorEnable, GPIO.LOW)
        print ("Stop")

#define main running section of code 
def main():
    directions = {'CW':1, 'CCW':-1, 'STOP':0}
    while True:
        while GPIO.input(microPinComp) == 0: #while loop for normal operation
            GPIO.output(LEDGreen, GPIO.LOW)
            if GPIO.input(BtnPinY) == 0:#left microswitch is not pressed
                motor(directions['CW'])
            else:
                motor(directions['STOP'])
            
        while GPIO.input(microPinRet) == 0:#right microswitch is pressed
            GPIO.output(LEDGreen, GPIO.HIGH) #while loop for screw extraction
            GPIO.output(LEDRed, GPIO.LOW)
            motor(directions['CCW'])
        GPIO.output(LEDRed, GPIO.HIGH)

#define destroy section for reset of pins and dissabling motor/leds
def destroy():
    GPIO.output(LEDRed, GPIO.HIGH)
    GPIO.output(MotorEnable, GPIO.LOW)
    GPIO.cleanup()
    
if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()