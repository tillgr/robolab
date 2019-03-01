import ev3dev.ev3 as ev3
import time


class LineFollower:
    #sensors
    ultrasonicSensor = ev3.UltrasonicSensor()
    colorSensor = ev3.ColorSensor()

    assert ultrasonicSensor.connected
    assert colorSensor.connected

    #motors
    leftMotor = ev3.LargeMotor('outB')
    rightMotor = ev3.LargeMotor('outC')

    assert leftMotor.connected
    assert rightMotor.connected

    # obstacle detection
    def obstacle(self):
        self.ultrasonicSensor.mode = 'US-DIST-CM'

        dist = self.ultrasonicSensor.value() // 10

        if dist < 5:
            self.leftMotor.run_timed(time_sp=3250, speed_sp=100, stop_action="coast")
            self.rightMotor.run_timed(time_sp=3250, speed_sp=100, stop_action="coast")
            time.sleep(3.25)
            return True
        else:
            return False

    # vertex detection
    def vertex(self):
        self.colorSensor.mode = 'COL-COLOR'

        if self.colorSensor.value() == 2 or self.colorSensor.value() == 5:
            print(f"color: {self.colorSensor.value()}")
            return True
        else:
            return False

    def drive(self):
        kp = 100   # kp*100 -> 10
        ki = 10    # ki*100 -> 1
        kd = 10  # kd*100 -> 100
        offset = 37
        tp = 60
        integral = 0
        lastError = 0
        derivative = 0

        t = 500

        while not self.obstacle():
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
            time.sleep(0.2)

            lastError = error
