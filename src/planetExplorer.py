#!/usr/bin/env python3
import time
from typing import Tuple

import lineFollower
import testingCommunication as communication
import odometry
import planet


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

    plan = planet.Planet()

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

    def convert_direction2(self, direction):
        if direction == 90:
            return planet.Direction.EAST
        elif direction == 0:
            return planet.Direction.NORTH
        elif direction == 270:
            return planet.Direction.WEST
        elif direction == 180:
            return planet.Direction.SOUTH

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
                print(f"corrected coords: {self.Xs}, {self.Ys} | {self.Xe}, {self.Ye}")
                weight = int(msg["payload"]["pathWeight"])

                self.plan.add_path(((self.Xs, self.Ys), self.convert_direction2(self.Ds)), ((self.Xe, self.Ye), self.convert_direction2(self.De)), weight)
                print("added path")

            elif msg["type"] == "unveiledPath":
                Xs = int(msg["payload"]["startX"])
                Ys = int(msg["payload"]["startY"])
                Ds = int(self.convert_direction(msg["payload"]["starDirection"]))

                Xe = int(msg["payload"]["endX"])
                Ye = int(msg["payload"]["endY"])
                De = int(self.convert_direction(msg["payload"]["endDirection"]))

                weight = int(msg["payload"]["pathWeight"])

                self.plan.add_path(((Xs, Ys), self.convert_direction2(Ds)),
                                   ((Xe, Ye), self.convert_direction2(De)), weight)
                print("added path")
                pass

            elif msg["type"] == "target":
                self.Xt = int(msg["payload"]["targetX"])
                self.Yt = int(msg["payload"]["targetY"])
                print("received target")

            elif msg["type"] == "pathSelect":
                self.Ds = int(self.convert_direction(msg["payload"]["startDirection"]))
                print("direction changed by server")

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

            # subscribe to planet channel the first time
            if self.first:
                com.sub_to_planet(self.planetName)

            # find paths and save them
            robot.explore(self.Ds)
            listPaths = robot.listPaths
            if self.first:
                listPaths.remove((self.Ds + 180) % 360)

            if self.Xt is not None and self.Yt is not None:
                print("Dijkstra")
                # TODO: run Dijkstra and get list with path, compare with actual list -> new shortest path
                self.Ds = int(input("Richtung, weil Dijkstra: "))

            # extract direction from list or choose path
            if len(self.listPath) is not 0:
                # TODO: use listPath for path selection, remove actual point
                # self.Ds = DIRECTION
                pass
            else:
                self.Ds = self.plan.random_direction(self.Xs, self.Ys, listPaths)
                # map explored ?
                self.plan.shorten_listUnvisitedPaths()
                if self.plan.exploration_finished() and not self.first:
                    break

            com.send_pathselection(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds))
            self.handle_messages(com.get_messages())
            com.clear_messages()

            robot.make_sound()

            robot.select_path(self.Ds)
            robot.drive()
            print(f"x: {self.Xs} y: {self.Ys}, d: {self.Ds}")
            calc.position(self.Ds, self.Xs, self.Ys, robot.get_distances())
            self.Xe = calc.x
            self.Ye = calc.y
            self.De = (robot.direction + 180) % 360
            print(f"direction End: {self.De}")

            # communication
            if robot.blocked:
                # TODO: direction?
                com.send_path(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds), str(self.Xs), str(self.Ys),
                              self.convert_direction(self.Ds), "blocked")
            else:
                com.send_path(str(self.Xs), str(self.Ys), self.convert_direction(self.Ds), str(self.Xe), str(self.Ye),
                              self.convert_direction(self.De), "free")

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

            print(f"facing: {self.Ds}")

            self.Xe = None
            self.Ye = None
            self.De = None

            self.first = False

            robot.set_direction(self.Ds)

        for i in range(3):
            robot.make_sound()
            time.sleep(1)
