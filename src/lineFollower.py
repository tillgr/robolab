#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time
import odometry
import math

class LineFollower:
    # sensors
    ultrasonicSensor = ev3.UltrasonicSensor()
    colorSensor = ev3.ColorSensor()
    gyroSensor = ev3.GyroSensor()

    assert ultrasonicSensor.connected
    assert colorSensor.connected
    assert gyroSensor.connected

    # motors
    leftMotor = ev3.LargeMotor('outB')
    rightMotor = ev3.LargeMotor('outC')

    assert leftMotor.connected
    assert rightMotor.connected

    # variables (n=0, e=90,...)
    direction = 0   # start direction always NORTH

    integral = 0
    lastError = 0
    derivative = 0

    listDistances = []

    red = (135, 60, 15)
    blue = (30, 150, 100)

    # get listDistances
    def getDistances(self):
        return self.listDistances

    # set & get direction
    def setDirection(self, direction):
        self.direction = direction

    def getDirection(self):
        return self.direction

    # turn
    def turn(self, deg, direction):
        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'
        self.leftMotor.command = 'run-direct'
        self.rightMotor.command = 'run-direct'

        if direction == "right":
            while self.gyroSensor.value() < deg:
                self.leftMotor.duty_cycle_sp = 20
                self.rightMotor.duty_cycle_sp = -20
        else:
            while abs(self.gyroSensor.value()) < deg:
                self.leftMotor.duty_cycle_sp = -20
                self.rightMotor.duty_cycle_sp = 20

        self.leftMotor.stop()
        self.rightMotor.stop()

    # obstacle detection
    def obstacle(self):
        self.ultrasonicSensor.mode = 'US-DIST-CM'
        self.colorSensor.mode = 'COL-REFLECT'

        dist = self.ultrasonicSensor.value() // 10

        if dist < 8:
            # ev3.Sound.speak("found an obstacle")
            self.lastError = 0
            self.integral = 0
            self.derivative = 0

            self.turn(90, "right")
            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            self.leftMotor.duty_cycle_sp = 20
            self.rightMotor.duty_cycle_sp = 20
            time.sleep(0.5)

            while self.colorSensor.value() not in range(30, 44):
                self.leftMotor.duty_cycle_sp = 20
                self.rightMotor.duty_cycle_sp = -20
            self.leftMotor.stop()
            self.rightMotor.stop()
            self.leftMotor.duty_cycle_sp = 0
            self.rightMotor.duty_cycle_sp = 0
            print("turned")

    # vertex detection
    def vertex(self):
        self.colorSensor.mode = 'RGB-RAW'

        color = self.colorSensor.bin_data('hhh')

        if (color[0] in range(self.red[0]-30, self.red[0]+30)) and (color[1] in range(self.red[1]-30, self.red[1]+30)) \
                and (color[2] in range(self.red[2]-30, self.red[2]+30)):
            print(f"color: {self.colorSensor.bin_data('hhh')}")
            return True
        elif (color[0] in range(self.blue[0]-30, self.blue[0]+30)) and (color[1] in range(self.blue[1]-30, self.blue[1]+30)) \
                and (color[2] in range(self.blue[2]-30, self.blue[2]+30)):
            print(f"color: {self.colorSensor.bin_data('hhh')}")
            return True
        else:
            return False

    # vertex exploration
    def explore(self, direction):
        self.leftMotor.command = 'run-direct'
        self.rightMotor.command = 'run-direct'

        self.leftMotor.duty_cycle_sp = 20
        self.rightMotor.duty_cycle_sp = 20
        time.sleep(1.1)
        if self.colorSensor.value() in range(30, 44):
            print(f"path, direction: {direction % 360}")
        self.leftMotor.duty_cycle_sp = -20
        self.rightMotor.duty_cycle_sp = -20
        time.sleep(1.1)

        self.leftMotor.duty_cycle_sp = 0

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'
        print(f"gyro: {self.gyroSensor.value()}")
        while abs(self.gyroSensor.value()) < 100:
            self.rightMotor.duty_cycle_sp = 20
            if self.colorSensor.value() in range(30, 44) and abs(self.gyroSensor.value()) > 50:
                print(f"path, direction: {(direction + 90) % 360}")
                break
        while self.gyroSensor.value() is not 0:
            self.rightMotor.duty_cycle_sp = -20
        self.rightMotor.stop()

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'
        while abs(self.gyroSensor.value()) < 100:
            self.leftMotor.duty_cycle_sp = 20
            if self.colorSensor.value() in range(30, 44) and abs(self.gyroSensor.value()) > 50:
                print(f"path, direction: {(direction - 90) % 360}")
                break
        while self.gyroSensor.value() is not 0:
            self.leftMotor.duty_cycle_sp = -20
        self.leftMotor.stop()

    # follow line
    def drive(self):
        kp = 30  # kp*100 -> 10
        ki = 1  # ki*100 -> 1
        kd = 10  # kd*100 -> 100
        offset = 37
        tp = 25

        positionLeft = self.leftMotor.position
        positionRight = self.rightMotor.position

        t = 500
        i = 0

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'

        self.listDistances.clear()

        while not self.vertex():


            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            #print(f"position left: {self.leftMotor.position}")
            #print(f"position right: {self.rightMotor.position}")

            self.colorSensor.mode = 'COL-REFLECT'
            lightValue = self.colorSensor.value()
            #print(f"lightValue: {lightValue}")
            error = lightValue - offset
            #print(f"error: {error}")
            self.integral += error
            #print(f"integral: {integral}")
            derivative = error - self.lastError
            #print(f"derivative: {derivative}")
            turn = (kp * error) + (ki * self.integral) + (kd * self.derivative)
            turn /= 100
            #print(f"turn: {turn}")
            powerLeft = tp + turn
            powerRight = tp - turn

            if powerLeft > 100:
                powerLeft = 100
            elif powerLeft < -100:
                powerLeft = -100

            if powerRight > 100:
                powerRight = 100
            elif powerRight < -100:
                powerRight = -100

            print(f"powerLeft: {powerLeft}")
            print(f"powerRight: {powerRight}")

            self.leftMotor.duty_cycle_sp = powerLeft
            self.rightMotor.duty_cycle_sp = powerRight

            self.lastError = error

            dl = 0.048 * (self.leftMotor.position - positionLeft)
            dr = 0.048 * (self.rightMotor.position - positionRight)

            positionLeft = self.leftMotor.position
            positionRight = self.rightMotor.position

            self.listDistances.append([dl, dr])

            self.obstacle()

        self.leftMotor.stop()
        self.rightMotor.stop()

        print(self.listDistances)