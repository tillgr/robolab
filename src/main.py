#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication
from driving import LineFollower
import time
import odometry

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
    cs.mode = 'RGB-RAW'
    us = ev3.UltrasonicSensor()
    us.mode = 'US-DIST-CM'

    print(f"color: {cs.bin_data('hhh')}")
    print(f"dist: {us.value()//10}")



    t = 200
    dist = 0
    pl = lm.position
    pr = rm.position

    print(f"position right: {rm.position}")

    '''
    for i in range(1):
        lm.run_timed(time_sp=t, speed_sp=100, stop_action="coast")
        rm.run_timed(time_sp=t, speed_sp=100, stop_action="coast")
        time.sleep(t/1000)
        print(f"position left: {lm.position}")
        print(f"position right: {rm.position}")

        dist += rm.position - pr

        pr = rm.position

    print(f"dist: {dist}")
    print(f"dist: {0.038 * dist}")
    

    lm.command = 'run-direct'
    rm.command = 'run-direct'

    lm.duty_cycle_sp = 50
    rm.duty_cycle_sp = 50

    time.sleep(1)
    lm.stop()
    rm.stop()
    '''

    robot = LineFollower()
    robot.drive()


# DO NOT EDIT
if __name__ == '__main__':
    run()
