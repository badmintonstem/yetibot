# Line Detection

import RPi.GPIO as GPIO  # Import the GPIO Library
import time  # Import the Time library

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

def driveRobot(leftMotor, rightMotor):
    print("left speed is", leftMotor, "Right speed is", rightMotor)

lineList = [["spin around",-1,1],["gentle left",0.7,1],["error",0,0],["hard left",0.5,1],["gentle right",1,0.7],["straight on",1,1],["hard right",1,0.5],["lost",0,0]]

try:
    # Repeat the next indented block forever
    while True:
        lineFollowList = []
        for sensor in sensors:
            lineFollowList.append(GPIO.input(sensor))
        lineResult = int("".join(str(i) for i in lineFollowList),2)
        print(lineFollowList, lineResult)
        #If the sensor is Low (=0), it's above the black line
        #driveRobot(lineList[lineResult][1],lineList[lineResult][2])

    # Wait, then do the same again
    time.sleep(0.2)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    GPIO.cleanup()
