#!/usr/bin/env python
# coding: Latin-1

# Simple example of a motor sequence script


# Import library functions we need
import ZeroBorg
import time
import math
import sys
import RPi.GPIO as GPIO  # Import the GPIO Library
from straight_line import *

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



# Set variables for the GPIO pins
pinLineFollowerCentre = 24
pinLineFollowerLeft = 23
pinLineFollowerRight = 25

# Set pin 25 as an input so we can read its value
GPIO.setup(pinLineFollowerCentre, GPIO.IN)
GPIO.setup(pinLineFollowerLeft, GPIO.IN)
GPIO.setup(pinLineFollowerRight, GPIO.IN)
sensors = [pinLineFollowerLeft,pinLineFollowerCentre,pinLineFollowerRight]

# Setup the ZeroBorg
ZB = ZeroBorg.ZeroBorg()
#ZB.i2cAddress = 0x44                  # Uncomment and change the value if you have changed the board address
ZB.Init()
if not ZB.foundChip:
    boards = ZeroBorg.ScanForZeroBorg()
    if len(boards) == 0:
        print('No ZeroBorg found, check you are attached :)')
    else:
        print('No ZeroBorg at address %02X, but we did find boards:' % (ZB.i2cAddress))
        for board in boards:
            print('    %02X (%d)' % (board, board))
        print('If you need to change the I²C address change the setup line so it is correct, e.g.')
        print('ZB.i2cAddress = 0x%02X' % (boards[0]))
    sys.exit()
#ZB.SetEpoIgnore(True)                 # Uncomment to disable EPO latch, needed if you do not have a switch / jumper
ZB.SetCommsFailsafe(False)             # Disable the communications failsafe
ZB.ResetEpo()

# Movement settings (worked out from our YetiBorg v2 on a smooth surface)
timeForward1m = 5.7                     # Number of seconds needed to move about 1 meter
timeSpin360   = 4.8                     # Number of seconds needed to make a full left / right spin
testMode = False                        # True to run the motion tests, False to run the normal sequence

# Power settings
voltageIn = 9.0                         # Total battery voltage to the ZeroBorg (change to 9V if using a non-rechargeable battery)
voltageOut = 6.0                        # Maximum motor voltage

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)

# Function to perform a general movement
def setDrive(driveLeft, driveRight):
    # Set the motors running
    ZB.SetMotor1(-driveRight * maxPower) # Rear right
    ZB.SetMotor2(-driveRight * maxPower) # Front right
    ZB.SetMotor3(-driveLeft  * maxPower) # Front left
    ZB.SetMotor4(-driveLeft  * maxPower) # Rear left

#List of motor speeds given sensor outputs
#lineList = [["spin around",-1,1],["gentle left",0.7,1],["error",0,0],["hard left",0.5,1],["gentle right",1,0.7],["straight on",1,1],["hard right",1,0.5],["lost",0,0]]
lineList = [["spin around",-1,1], ["hard right",1,0.5], ["straight on",1,1], ["gentle right",1,0.7], ["hard left",0.5,1], ["error",0,0], ["gentle left",0.7,1],["lost",0,0]]

if __name__ == "__main__":
    try:
        # Repeat the next indented block forever
        while True:
            a = get_walls()
            motorspeeds = speed_calc(a,full_speed)
            setDrive(motorspeeds[0],motorspeeds[1])

            # Wait, then do the same again
            #time.sleep(0.2)

    # If you press CTRL+C, cleanup and stop
    except KeyboardInterrupt:
        setDrive(0,0)
        print("quitting")
        tof1.stop_ranging()
        tof2.stop_ranging()
        sys.exit()
