#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
import time
from planet import Direction, Planet
from communication import Communication
from odometry import LineFollower

client = None  # DO NOT EDIT


def run():
    # DO NOT EDIT
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER

    rightMotor = ev3.LargeMotor('outC')
    leftMotor = ev3.LargeMotor('outB')
    leftMotor.duty_cycle_sp = 80

    start = time.time()

    while time.time()-start < 10:
        continue

    leftMotor.stop()

    cs = ev3.ColorSensor()
    cs.mode = 'COL-COLOR'
    print("Hello World, it works!")
    print(cs.value())

# DO NOT EDIT
if __name__ == '__main__':
    run()
