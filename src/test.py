#!/usr/bin/env python3

import driving
import communication


class Test:
    def firstVertex(self, c):
        robot = driving.LineFollower
        robot.drive()
        com = communication.Communication(c)
