#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

import ev3dev.ev3 as ev3

class LineFollower():
    def __init__(self):
        stop = False

    def drive(self):
        stop = False

        #sensors
        colorSensor = ev3.ColorSensor()
        ultrasonicSensor = ev3.UltrasonicSensor()

        assert colorSensor.connected
        assert ultrasonicSensor.connected

        #motors
        rightMotor = ev3.LargeMotor(ev3.OUTPUT_C)
        leftMotor = ev3.LargeMotor(ev3.OUTPUT_B)

        assert rightMotor.connected
        assert leftMotor.connected

        while(not stop):
            #drive


class Odometry():
    #code

if __name__ == "__main__":
    #run LineFollower