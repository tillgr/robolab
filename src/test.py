#!/usr/bin/env python3

import lineFollower
import testingCommunication as communication
import odometry


class Test:
    Xs = None      # start x,y
    Ys = None
    Ds = 0      # direction
    De = None
    Xe = None      # end x,y
    Ye = None
    Xt = None
    Yt = None

    finished = False

    def __init__(self):
        pass

    # convert direction
    def convert_direction(self, direction):
        if direction == 90:
            return "E"
        elif direction == 0:
            return "N"
        elif direction == 270:
            return "W"
        elif direction == 180:
            return "S"

        elif direction == "E":
            return 90
        elif direction == "N":
            return 0
        elif direction == "S":
            return 180
        elif direction == "W":
            return 270

    # handle messages
    def handle_messages(self, messages):
        for msg in messages:
            if msg["type"] == "path":
                self.Xe = msg["payload"]["endX"]
                self.Ye = msg["payload"]["endY"]
                self.De = msg["payload"]["endDirection"]
            elif msg["type"] == "unveiledPath":
                # add to map
                pass
            elif msg["type"] == "target":
                self.Xt = int(msg["payload"]["targetX"])
                self.Yt = int(msg["payload"]["targetY"])

    def target_reached(self):
        if self.Xe == self.Xt and self.Ye == self.Yt:
            com.send_targetreached(self)
            self.finished = True

            # main function
    def run(self, c):
        robot = lineFollower.LineFollower()
        calc = odometry.Odometry()

        # drive to first vertex
        robot.drive()

        com = communication.Communication(c)

        # handle first messages
        for msg in com.get_messages():
            # get start coordinates
            if msg["type"] == "planet":
                self.Xs = int(msg["payload"]["startX"])
                self.Ys = int(msg["payload"]["startY"])
            elif msg["type"] == "unveiledPath":
                # add to map
                pass
            elif msg["type"] == "target":
                self.Xt = int(msg["payload"]["targetX"])
                self.Yt = int(msg["payload"]["targetY"])
        com.clear_messages()

        while not self.finished:
            robot.explore(self.Xs)

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



