#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

import ev3dev.ev3 as ev3


class LineFollower:
    def __init__(self):
        stop = False

    def drive(self):
        stop = True

        # sensors
        colorSensor = ev3.ColorSensor()
        ultrasonicSensor = ev3.UltrasonicSensor()

        assert colorSensor.connected
        assert ultrasonicSensor.connected

        colorSensor.mode = 'COL-REFLECT'
        ultrasonicSensor.mode = 'US-DIST-CM'

        # motors
        rightMotor = ev3.LargeMotor(ev3.OUTPUT_C)
        leftMotor = ev3.LargeMotor(ev3.OUTPUT_B)

        assert rightMotor.connected
        assert leftMotor.connected

        kp = 1000   # kp*100 -> 10
        ki = 100    # ki*100 -> 1
        kd = 10000  # kd*100 -> 100
        offset = 45
        tp = 50
        integral = 0
        lastError = 0
        derivative = 0

        time = 500

        while not stop:
            lightValue = colorSensor.value()
            error = lightValue - offset
            integral += error
            derivative = error - lastError
            turn = (kp * error) + (ki * integral) + (kd * derivative)
            turn /= 100
            powerLeft = tp + turn
            powerRight = tp - turn

            leftMotor.run_timed(time_sp=time, speed_sp=powerLeft, stop_action="coast")
            rightMotor.run_timed(time_sp=time, speed_sp=powerRight, stop_action="coast")

            lastError = error

        rightMotor.run_timed(time_sp=600)
        leftMotor.run_timed(time_sp=600)


class Odometry():
    x=42


if __name__ == "__main__":
    robot = LineFollower()
    robot.drive()
