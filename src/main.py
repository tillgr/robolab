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

    cs = ev3.ColorSensor()

    cs.mode = 'RGB-RAW'

    col = cs.bin_data('hhh')

    print(col)


    robot = LineFollower()


    inp = input("calibrate? (yes/no)")
    if inp == "yes":
        robot.calibrate()
        time.sleep(10)


    robot.drive()
    calc = odometry.Odometry()
    calc.position(0, 0, 0, robot.get_distances())
    robot.set_direction(calc.get_direction())
    print(calc.get_position())
    print(f"direction: {robot.get_direction()}")

    robot.explore(robot.get_direction())

    inp = input("dir: ")

    robot.select_path(int(inp))
    robot.set_direction(int(inp))
    robot.drive()
    calc.position(robot.get_direction(), 0, 0, robot.get_distances())

    t = test.Test()
    #t.first_vertex(client)

# DO NOT EDIT
if __name__ == '__main__':
    run()
