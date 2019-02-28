#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

import ev3dev.ev3 as ev3
import time


class LineFollower:
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
        leftMotor = ev3.LargeMotor('outB')
        rightMotor = ev3.LargeMotor('outC')

        assert leftMotor.connected
        assert rightMotor.connected

        dist = ultrasonicSensor.value()//10

        kp = 1000   # kp*100 -> 10
        ki = 100    # ki*100 -> 1
        kd = 10000  # kd*100 -> 100
        offset = 45
        tp = 50
        integral = 0
        lastError = 0
        derivative = 0

        t = 500

        while dist > 5:
            lightValue = colorSensor.value()
            print(f"lightValue: {lightValue}")
            error = lightValue - offset
            print(f"error: {error}")
            integral += error
            print(f"integral: {integral}")
            derivative = error - lastError
            print(f"derivative: {derivative}")
            turn = (kp * error) + (ki * integral) + (kd * derivative)
            turn /= 100
            print(f"turn: {turn}")
            powerLeft = tp + turn
            print(f"powerLeft: {powerLeft}")
            powerRight = tp - turn
            print(f"powerRight: {powerRight}")

            if powerLeft > 100:
                powerLeft = 100
            elif powerLeft < -100:
                powerLeft = -100

            if powerRight > 100:
                powerRight = 100
            elif powerRight < -100:
                powerRight = -100

            leftMotor.run_timed(time_sp=500, speed_sp=powerLeft, stop_action="coast")
            rightMotor.run_timed(time_sp=500, speed_sp=powerRight, stop_action="coast")

            lastError = error

        rightMotor.run_timed(time_sp=5000, speed_sp=100, stop_action="coast")
        leftMotor.run_timed(time_sp=5000, speed_sp=-100, stop_action="coast")
        time.sleep(5)
        print("odometry works")


class Odometry():
    x=42


if __name__ == "__main__":
    robot = LineFollower()
    robot.drive()
