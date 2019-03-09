#!/usr/bin/env python3
import time

import lineFollower
import testingCommunication as communication
import odometry


class PlanetExplorer:
    Xs = None      # start x,y
    Ys = None
    Ds = 0      # direction
    De = None
    Xe = None      # end x,y
    Ye = None
    Xt = None
    Yt = None

    listPath = []

    planetName = ""
    first = True
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
            if msg["type"] == "planet":

                self.Xs = int(msg["payload"]["startX"])
                self.Ys = int(msg["payload"]["startY"])
                self.planetName = msg["payload"]["planetName"]

            elif msg["type"] == "path":
                self.Xe = int(msg["payload"]["endX"])
                self.Ye = int(msg["payload"]["endY"])
                self.De = int(self.convert_direction(msg["payload"]["endDirection"]))

                weight = int(msg["payload"]["pathWeight"])

                # TODO: add to map (((self.Xs, self.Ys), self.Ds), ((Xe, Ye), De)) with weight

            elif msg["type"] == "unveiledPath":
                # add to map
                pass

            elif msg["type"] == "target":
                self.Xt = int(msg["payload"]["targetX"])
                self.Yt = int(msg["payload"]["targetY"])

            elif msg["type"] == "pathSelect":
                self.Ds = int(self.convert_direction(msg["payload"]["startDirection"]))

            elif msg["type"] == "done":
                self.finished = True

    def target_reached(self):
        if self.Xe == self.Xt and self.Ye == self.Yt:
            return True
        else:
            return False

            # main function
    def run(self, c):
        robot = lineFollower.LineFollower()
        calc = odometry.Odometry()
        com = communication.Communication(c)

        # drive to first vertex
        robot.drive()

        com.init_connection()
        robot.make_sound()

        while not self.finished:
            # deal with received messages
            self.handle_messages(com.get_messages())
            com.clear_messages()

            if self.first:
                com.sub_to_planet(self.planetName)
                self.first = False

            # find paths and save them
            robot.explore(self.Ds)
            # TODO: add possible directions to planet

            # map explored ?
            # TODO: using planet class to check if map is explored

            if self.Xt is not None and self.Yt is not None:
                print("Dijkstra")
                # TODO: run Dijkstra and get list with path, compare with actual list -> new shortest path
                pass

            # extract direction from list or choose path
            if len(self.listPath) is not 0:
                # TODO: use listPath for path selection, remove actual point
                # self.Ds = DIRECTION
                pass
            else:
                # TODO: get direction from planet
                inp = input("dir: ")
                self.Ds = int(inp)
                print(f"robot direction: {robot.get_direction()}")

            com.send_pathselection(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds))
            self.handle_messages(com.get_messages())
            com.clear_messages()

            robot.make_sound()

            robot.select_path(self.Ds)
            robot.set_direction(self.Ds)
            robot.drive()
            calc.position(self.Ds, self.Xs, self.Ys, robot.get_distances())
            self.Xe = calc.x
            self.Ye = calc.y
            self.De = robot.direction

            # communication
            if robot.blocked:
                # TODO: right direction?
                com.send_path(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds), str(self.Xs), str(self.Ys),
                              self.convert_direction(self.Ds), "blocked")
            else:
                com.send_path(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds), str(self.Xe), str(self.Ye),
                              self.convert_direction((self.De+180)%360), "free")

            self.handle_messages(com.get_messages())
            com.clear_messages()

            # target reached ?
            if self.target_reached():
                com.send_targetreached()
                self.handle_messages(com.get_messages())
                com.clear_messages()
                if self.finished:
                    break
                else:
                    pass

            # update variables
            self.Xs = self.Xe
            self.Ys = self.Ye
            self.Ds = (self.De + 180) % 360

            robot.set_direction(self.Ds)

            self.Xe = None
            self.Ye = None
            self.De = None

        for i in range(3):
            robot.make_sound()
            time.sleep(1)
