#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
import time
from planet import Direction, Planet
from communication import Communication
from lineFollower import LineFollower
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

    rm = ev3.LargeMotor('outC')
    lm = ev3.LargeMotor('outB')

    robot = LineFollower()
    robot.drive()
    calc = odometry.Odometry()
    calc.position(270, 0, 0, robot.getDistances())
    robot.setDirection(calc.getDirection())
    print(calc.getPosition())
    print(robot.getDirection())
    robot.explore(robot.getDirection())

    t = test.Test()
    #t.firstVertex(client)

# DO NOT EDIT
if __name__ == '__main__':
    run()
