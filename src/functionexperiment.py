import random

import communication


def directions(dir):
    if dir==90 :
        return "E"
    elif dir==0:
        return "N"
    elif dir==270:
        return "W"
    elif dir==180:
        return "S"

    elif dir=="E":
        return 90
    elif dir=="N":
        return 0
    elif dir=="S":
        return 180
    elif dir=="W":
        return 270

def target_reached():
    if self.Xe == self.Xt and self.Ye == self.Yt:
        com.send_targetreached(self)
        self.finished = True

    elif i["type"] == "unveiledPath":
        Xs = int(msg["payload"]["startX"])
        Ys = int(msg["payload"]["startY"])
        Xe = int(msg["payload"]["endX"])
        Ye = int(msg["payload"]["endY"])
        Ds = msg["payload"]["starDirection"]
        De = msg["payload"]["endDirection"]
        status = msg["payload"]["pathStatus"]
        weight = msg["payload"]["pathWeight"]

listUnvisitedPaths = []

def random_direction(self, x, y, listDirections = []):
    listDirectionsCopy = listDirections.copy()

    for item in listDirectionsCopy:
        d = None
        if item == 0 :
            d = Direction.NORTH
        elif item == 90:
            d = Direction.EAST
        elif item == 180:
            d = Direction.SOUTH
        elif item == 270:
            d = Direction.WEST

        for direction in self.planetPaths[(x,y)].items():
            if direction[0] == d:
                del d

    if len(listDirectionsCopy) == 0:
        choice = random.choice(listDirections)
        return choice

    else:
        choice = random.choice(listDirectionsCopy)

        listDirectionsCopy.remove(choice)

        for direction in listDirectionsCopy:
            self.listUnvisitedPaths.append([(x,y),listDirectionsCopy])
        return choice

def shorten_listUnvisitedPaths(self):
    for path in self.listUnvisitedPaths:
        for direction in self.planetPaths[path[0]].items():
            if path[1] == direction[0]:
                self.listUnvisitedPaths.remove(path)

def exploration_finished(self):
    if len(self.listUnvisitedPaths) == 0:
        return True
    else:
        return False
