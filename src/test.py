#!/usr/bin/env python3

import lineFollower
import communication


class Test:
    def firstVertex(self, c):
        robot = lineFollower.LineFollower()
        robot.drive()
        com = communication.Communication(c)
