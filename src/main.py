#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication
from driving import LineFollower
import time

client = None  # DO NOT EDIT


def run():
    # DO NOT EDIT
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER

    rm = ev3.LargeMotor('outC')
    lm = ev3.LargeMotor('outB')
    cs = ev3.ColorSensor()
    cs.mode = 'COL-COLOR'
    us = ev3.UltrasonicSensor()
    us.mode = 'US-DIST-CM'

    assert rm.connected

    print(f"color: {cs.value()}")
    print(f"dist: {us.value()//10}")



    t = 3250
    #lm.run_timed(time_sp=t, speed_sp=100, stop_action="coast")
    #rm.run_timed(time_sp=t, speed_sp=-100, stop_action="coast")
    #time.sleep(t/1000)

    robot = LineFollower()
    robot.drive()


# DO NOT EDIT
if __name__ == '__main__':
    run()
