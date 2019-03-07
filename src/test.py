#!/usr/bin/env python3

import lineFollower
import testingCommunication as communication
import odometry


class Test:
    Xs = 0      # start x,y
    Ys = 0
    Ds = 0      # direction
    De = 0
    Xe = 0      # end x,y
    Ye = 0
    Xt = 0
    Yt = 0

    def __init__(self):
        pass

    def run(self, c):
        robot = lineFollower.LineFollower()
        calc = odometry.Odometry()

        robot.drive()

        com = communication.Communication(c)

        for i in com.get_messages():
            # get start coordinates
            if i["type"] == "planet":
                self.Xs = int(i["payload"]["startX"])
                self.Ys = int(i["payload"]["startY"])
            elif i["type"] == "unveiledPath":
                # add to map
                pass
            elif i["type"] == "target":
                self.Xt = int(i["payload"]["targetX"])
                self.Y,t = int(i["payload"]["targetY"])

        robot.explore(0)

        inp = input("dir: ")

        com.send_pathselection(str(self.Xs), str(self.Ys), "N")

        robot.select_path(int(inp))
        robot.set_direction(int(inp))
        robot.drive()
        calc.position(robot.get_direction(), self.Xs, self.Ys, robot.get_distances())
        self.Xe = calc.x
        self.Ye = calc.y
        self.De = robot.direction

        com.send_path(str(self.Xs), str(self.Ys), "N", str(self.Xe), str(self.Ye), "N", "free")



