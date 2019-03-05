#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication
from driving import LineFollower
import time
import odometry
import test
import communication

client = None  # DO NOT EDIT


def run():
    # DO NOT EDIT
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    gs = ev3.GyroSensor()
    gs.mode = "GYRO-RATE"
    gs.mode = "GYRO-ANG"

    rm = ev3.LargeMotor('outC')
    lm = ev3.LargeMotor('outB')

    pl = lm.position
    pr = rm.position

    print(f"position right: {rm.position}")

    #lm.run_to_rel_pos(position_sp=360, speed_sp=40, stop_action="hold")
    #rm.run_to_rel_pos(position_sp=360, speed_sp=40, stop_action="hold")

    #time.sleep(10)

    print(f"position right: {rm.position}")

    robot = LineFollower()
    #robot.drive()

    t = test.Test()
    t.firstVertex(client)


# DO NOT EDIT
if __name__ == '__main__':
    run()
