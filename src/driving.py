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

        kp = 100   # kp*100 -> 10
        ki = 10    # ki*100 -> 1
        kd = 10  # kd*100 -> 100
        offset = 37
        tp = 60
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

            leftMotor.run_timed(time_sp=500, speed_sp=powerLeft, stop_action="coast")
            rightMotor.run_timed(time_sp=500, speed_sp=powerRight, stop_action="coast")
            time.sleep(0.2)

            lastError = error

            dist = ultrasonicSensor.value() // 10