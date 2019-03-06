#!/usr/bin/env python3

import lineFollower
import communication


class Test:
    Xs = 0
    Ys = 0
    direction = 0
    Xe = 0
    Ye = 0

    def first_vertex(self, c):
        robot = lineFollower.LineFollower()
        robot.drive()
        com = communication.Communication(c)
        # get start position from server
        self.Xs = com.startX
        self.Ys = com.startY

