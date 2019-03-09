#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt

import planetExplorer
from lineFollower import LineFollower
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

    robot = LineFollower()

    inp = input("calibrate? (y/n)")
    if inp == "y":
        robot.calibrate()
        time.sleep(10)


    #robot.drive()
    #robot.drive(float(input("p: ")), float(input("i: ")), float(input("d: ")), float(input("v: ")))
    #robot.explore(robot.direction)


    pe = planetExplorer.PlanetExplorer()
    pe.run(client)

# DO NOT EDIT
if __name__ == '__main__':
    run()
