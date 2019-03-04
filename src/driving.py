#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time


class LineFollower:
    # sensors
    ultrasonicSensor = ev3.UltrasonicSensor()
    colorSensor = ev3.ColorSensor()

    assert ultrasonicSensor.connected
    assert colorSensor.connected

    # motors
    leftMotor = ev3.LargeMotor('outB')
    rightMotor = ev3.LargeMotor('outC')

    assert leftMotor.connected
    assert rightMotor.connected

    # variables (n=0, e=90,...)
    direction = 0   # start direction always NORTH

    listDistances = list()

    red = (135, 60, 15)
    blue = (30, 150, 100)

    # obstacle detection
    def obstacle(self):
        self.ultrasonicSensor.mode = 'US-DIST-CM'
        self.colorSensor.mode = 'COL-REFLECT'

        dist = self.ultrasonicSensor.value() // 10

        if dist < 15:
            # ev3.Sound.speak("found an obstacle")
            self.leftMotor.run_timed(time_sp=1000, speed_sp=100, stop_action="coast")
            self.rightMotor.run_timed(time_sp=1000, speed_sp=-100, stop_action="coast")
            time.sleep(0.9)
            while self.colorSensor.value() not in range(30, 44):
                self.leftMotor.run_timed(time_sp=300, speed_sp=100, stop_action="coast")
                self.rightMotor.run_timed(time_sp=300, speed_sp=-100, stop_action="coast")
                time.sleep(0.1)

    # vertex detection
    def vertex(self):
        self.colorSensor.mode = 'RGB-RAW'

        color = self.colorSensor.bin_data('hhh')

        if (color[0] in range(self.red[0]-30, self.red[0]+30)) and (color[1] in range(self.red[1]-30, self.red[1]+30)) and (color[2] in range(self.red[2]-30, self.red[2]+30)):
            print(f"color: {self.colorSensor.bin_data('hhh')}")
            return True
        elif (color[0] in range(self.blue[0]-30, self.blue[0]+30)) and (color[1] in range(self.blue[1]-30, self.blue[1]+30)) and (color[2] in range(self.blue[2]-30, self.blue[2]+30)):
            print(f"color: {self.colorSensor.bin_data('hhh')}")
            return True
        else:
            return False

    # vertex exploration

    def drive(self):
        kp = 100  # kp*100 -> 10
        ki = 10  # ki*100 -> 1
        kd = 100  # kd*100 -> 100
        offset = 37
        tp = 90
        integral = 0
        lastError = 0
        derivative = 0

        t = 500

        while not self.vertex():
            print(f"position left: {self.leftMotor.position}")
            print(f"position right: {self.rightMotor.position}")

            self.colorSensor.mode = 'COL-REFLECT'
            lightValue = self.colorSensor.value()
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

            self.leftMotor.run_timed(time_sp=500, speed_sp=powerLeft, stop_action="coast")
            self.rightMotor.run_timed(time_sp=500, speed_sp=powerRight, stop_action="coast")
            time.sleep(0.3)

            lastError = error

            dl = 0
            dr = 0
            self.listDistances.append((dl, dr))
            self.obstacle()

        return self.listDistances
