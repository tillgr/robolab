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

    # variables
    direction = 0   # start direction always NORTH
    x = 0
    y = 0
    offset = 170 #141

    integral = 0
    lastError = 0
    derivative = 0

    listDistances = []
    listPaths = []

    blocked = False

    red = (135, 60, 15)
    blue = (30, 150, 100)

    # get listDistances
    def get_distances(self):
        return self.listDistances

    # set & get direction
    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_pathstatus(self):
        return self.pathStatus

    def calibrate(self):
        self.colorSensor.mode = 'RGB-RAW'
        valueWhite = 0
        valueBlack = 0
        for i in range(3):
            inp = input("White: ")
            color = self.colorSensor.bin_data('hhh')
            valueWhite += (color[0] + color[1] + color[2])/3
            print(f"white: {valueWhite}")
        for i in range(3):
            inp = input("Black: ")
            color = self.colorSensor.bin_data('hhh')
            valueWhite += (color[0] + color[1] + color[2])/3
            print(f"black: {valueBlack}")
        valueWhite /= 3
        valueBlack /= 3
        self.offset = (valueBlack + valueWhite)/2
        print(f"offset: {self.offset}")

    def make_sound(self):
        ev3.Sound.beep()


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

        dist = self.ultrasonicSensor.value() // 10

        if dist < 14:
            ev3.Sound.beep()
            self.blocked = True

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
            print("Found blocked path")

    # vertex detection
    def vertex(self):
        self.colorSensor.mode = 'RGB-RAW'

        color = self.colorSensor.bin_data('hhh')

        if (color[0] in range(self.red[0]-30, self.red[0]+30)) and (color[1] in range(self.red[1]-30, self.red[1]+30)) \
                and (color[2] in range(self.red[2]-30, self.red[2]+30)):
            return True
        elif (color[0] in range(self.blue[0]-30, self.blue[0]+30)) and (color[1] in range(self.blue[1]-30, self.blue[1]+30)) \
                and (color[2] in range(self.blue[2]-30, self.blue[2]+30)):
            return True
        else:
            return False

    # vertex exploration
    def explore(self, direction):
        self.listPaths.clear()
        self.listPaths.append((direction + 180) % 360)
        self.rightMotor.run_to_rel_pos(position_sp=100, speed_sp=150)
        self.leftMotor.run_to_rel_pos(position_sp=100, speed_sp=150)
        time.sleep(1.5)

        self.leftMotor.command = 'run-direct'
        self.rightMotor.command = 'run-direct'

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'

        self.colorSensor.mode = 'RGB-RAW'

        t90 = False
        t270 = False
        t360 = False

        while abs(self.gyroSensor.value()) < 380:
            self.rightMotor.run_to_rel_pos(position_sp=-10, speed_sp=150)
            self.leftMotor.run_to_rel_pos(position_sp=10, speed_sp=150)
            time.sleep(0.01)
            color = self.colorSensor.bin_data('hhh')

            if self.gyroSensor.value() in range(70, 110) and int((color[0] + color[1] + color[2]) / 3) < 50 and not t90:
                print(f"path, direction: {(direction + 90) % 360}")
                self.listPaths.append((direction + 90) % 360)
                t90 = True

            if self.gyroSensor.value() in range(250, 290) and int((color[0] + color[1] + color[2]) / 3) < 50 and not t270:
                print(f"path, direction: {(direction - 90) % 360}")
                self.listPaths.append((direction - 90) % 360)
                t270 = True

            if self.gyroSensor.value() in range(340, 380) and int((color[0] + color[1] + color[2]) / 3) < 50 and not t360:
                print(f"path, direction: {direction}")
                self.listPaths.append(direction)
                t360 = True

        self.leftMotor.stop()
        self.rightMotor.stop()

    #select path
    def select_path(self, direction):
        self.leftMotor.command = 'run-direct'
        self.rightMotor.command = 'run-direct'

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'

        if direction == self.direction:
            while abs(self.gyroSensor.value()) < 40:
                self.rightMotor.run_to_rel_pos(position_sp=10, speed_sp=150)
                self.leftMotor.run_to_rel_pos(position_sp=-10, speed_sp=150)

            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            color = self.colorSensor.bin_data('hhh')
            color = int((color[0] + color[1] + color[2]) / 3)
            while color not in range(self.offset - 30, self.offset + 30):
                self.rightMotor.duty_cycle_sp = -15
                self.leftMotor.duty_cycle_sp = 15
                color = self.colorSensor.bin_data('hhh')
                color = int((color[0] + color[1] + color[2]) / 3)

            self.rightMotor.stop()
            self.leftMotor.stop()

        elif direction == (self.direction + 90) % 360:
            while abs(self.gyroSensor.value()) < 40:
                self.rightMotor.run_to_rel_pos(position_sp=-10, speed_sp=150)
                self.leftMotor.run_to_rel_pos(position_sp=10, speed_sp=150)

            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            color = self.colorSensor.bin_data('hhh')
            color = int((color[0] + color[1] + color[2]) / 3)
            while color not in range(self.offset - 30, self.offset + 30):
                self.rightMotor.duty_cycle_sp = -15
                self.leftMotor.duty_cycle_sp = 15
                color = self.colorSensor.bin_data('hhh')
                color = int((color[0] + color[1] + color[2]) / 3)

            self.rightMotor.stop()
            self.leftMotor.stop()

        elif direction == (self.direction - 90) % 360:
            while abs(self.gyroSensor.value()) < 120:
                self.rightMotor.run_to_rel_pos(position_sp=10, speed_sp=150)
                self.leftMotor.run_to_rel_pos(position_sp=-10, speed_sp=150)

            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            color = self.colorSensor.bin_data('hhh')
            color = int((color[0] + color[1] + color[2]) / 3)
            while color not in range(self.offset - 30, self.offset + 30):
                self.rightMotor.duty_cycle_sp = -15
                self.leftMotor.duty_cycle_sp = 15
                color = self.colorSensor.bin_data('hhh')
                color = int((color[0] + color[1] + color[2]) / 3)

            self.rightMotor.stop()
            self.leftMotor.stop()

        elif direction == (self.direction + 180) % 360:
            while abs(self.gyroSensor.value()) < 120:
                self.rightMotor.run_to_rel_pos(position_sp=-10, speed_sp=150)
                self.leftMotor.run_to_rel_pos(position_sp=10, speed_sp=150)

            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            color = self.colorSensor.bin_data('hhh')
            color = int((color[0] + color[1] + color[2]) / 3)
            while color not in range(self.offset - 30, self.offset + 30):
                self.rightMotor.duty_cycle_sp = -15
                self.leftMotor.duty_cycle_sp = 15
                color = self.colorSensor.bin_data('hhh')
                color = int((color[0] + color[1] + color[2]) / 3)

            self.leftMotor.stop()
            self.rightMotor.stop()

    # follow line
    def drive(self, p=11, i=0.8, d=8, v=35):
        kp = p       # 8
        ki = i       # 1
        kd = d       # 4
        tp = v       # 20

        self.blocked = False

        positionLeft = self.leftMotor.position
        positionRight = self.rightMotor.position

        self.gyroSensor.mode = 'GYRO-RATE'
        self.gyroSensor.mode = 'GYRO-ANG'

        self.listDistances.clear()

        while not self.vertex():
            self.leftMotor.command = 'run-direct'
            self.rightMotor.command = 'run-direct'

            self.colorSensor.mode = 'RGB-RAW'
            color = self.colorSensor.bin_data('hhh')
            lightValue = int((color[0]+color[1]+color[2])/3)
            error = lightValue - self.offset
            self.integral += error
            self.derivative = error - self.lastError
            turn = (kp * error) + (ki * self.integral) + (kd * self.derivative)
            turn /= 100
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
