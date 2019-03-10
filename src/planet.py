#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict
import pprint
import random
import copy



# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

@unique
class Direction(IntEnum):  # Richtung
    """ Directions in degrees """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


# simple alias, no magic here
Weight = int  # gewicht der kanten
""" 
    Weight of a given path (received from the server)
    value:  -1 if broken path 
            >0 for all other paths
            never 0
"""


class SPath:
    start: Tuple[int, int]
    target: Tuple[int, int]
    weight: int
    path: List[Tuple[Tuple[int, int], Direction]]
    direction: Direction


    def __init__(self):
        self.weight = None
        self.start = None #Tuple[int, int]
        self.target = None #Tuple[int, int]
        self.weight = None #int
        self.path = [] #List[Tuple[Tuple[int, int], Direction]]
        self.direction = None


class Planet:  # Karte
    """
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """
    index = None

    def __init__(self):
        """ Initializes the data structure """
        self.planetKarte = []  # pfadpaare
        self.planetPaths = {}  # eigentliche karte
        self.paths = {}  # hile für einfügen in karte
        self.target = None  # routenziel
        self.listUnvisitedPaths = []
        self.planetPaths_ublocked = {}  # karte ohne geblockte pfade


    def direction_invert(self, direction):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        if direction == Direction.EAST:
            return Direction.WEST
        if direction == Direction.SOUTH:
            return Direction.NORTH
        if direction == Direction.WEST:
            return Direction.EAST

    def random_direction(self, x, y, listDirections):   # wählt neuen pfad für erkundung
        listDirectionsCopy = listDirections.copy()
        listLoops = []

        print(listDirectionsCopy)

        for item in listDirectionsCopy:
            d = None
            if item == 0:
                d = Direction.NORTH
            elif item == 90:
                d = Direction.EAST
            elif item == 180:
                d = Direction.SOUTH
            elif item == 270:
                d = Direction.WEST

            try:
                for path in self.planetPaths[(x, y)].items():
                    if path[0] == d:
                        listDirectionsCopy.remove(d)
                        print(f"removed {d}")
                    if path[1][0] == (x, y):
                        listLoops.append(path[0].value)
                        print(f"added {path[0].value} to list loops")
            except:
                pass

        if len(listDirectionsCopy) == 0:
            for i in listLoops:
                listDirections.remove(i)

            choice = random.choice(listDirections)
            print("random choice")
            return choice

        else:
            print(f"chose from {listDirectionsCopy}")
            self.listUnvisitedPaths.append(listDirectionsCopy)
            choice = random.choice(listDirectionsCopy)
            return choice

    def shorten_listUnvisitedPaths(self):   #löscht schon gewählte pfade
        for path in self.listUnvisitedPaths:
            try:
                for direction in self.planetPaths[path[0]].items():
                    if path[1] == direction[0]:
                        self.listUnvisitedPaths.remove(path)
                        print(f"shortened path list, removed {path}")
            except:
                pass


    def exploration_finished(self):
        if len(self.listUnvisitedPaths) == 0:
            return True
        else:
            return False

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):  # Koordinaten, Hin/Rückrichtung

        self.planetKarte.append([start, target, weight])
        # print(f"Start: {start}")

        # print(self.planetKarte)
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it
        example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """

        for start, target, weight in self.planetKarte:
            if start[0] not in self.planetPaths.keys():
                self.paths = {start[1]: (target[0], target[1], weight)}  # ansonsten neuen key anlegen
                self.planetPaths.update({start[0]: self.paths})  # richtung adden
            else:  # wenn knoten in dict, richtung adden
                self.planetPaths[start[0]].update({start[1]: (target[0], target[1], weight)})
                # self.planetPaths.update({start[0] : self.paths})

            # rückrichtung

            if target[0] not in self.planetPaths.keys():
                self.paths = {target[1]: (start[0], start[1], weight)}
                self.planetPaths.update({target[0]: self.paths})
            else:
                self.planetPaths[target[0]].update({target[1]: (start[0], start[1], weight)})

        #for k, v in self.planetPaths:
        #    for val in v.values:
        #        print(val)

        pass
        # print("karte")
        # pprint.pprint(self.planetKarte)
        # print("Paths")
        # pprint.pprint(self.planetPaths)

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        ''' [[((0, 0), < Direction.NORTH: 0 >), ((0, 1), < Direction.SOUTH: 180 >), 1]
            [((0, 0), <Direction.EAST: 90>), ((1, 0), <Direction.WEST: 270>), 1]'''

        """
        Returns all paths
        example:
            get_paths() returns:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """
        # print(self.planetPaths.items())
        # print(self.planetPaths)
        return self.planetPaths

        pass
    '''
    def update_weight(self, tupel: Tuple[Direction, Tuple[Tuple[int, int], Direction, Weight]], new_value: int):
        lst = list(tupel)
        lst2 = list(lst[1])
        lst2[2] = new_value

        lst[1] = tuple(lst2)
        tupel = tuple(lst)
        # print(tupel)
        return tupel
    '''

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[
        List[Tuple[Tuple[int, int], Direction]]]:

        start_save = start
        besucht = []
        aListe = []     #arbeitsliste

        #p = SPath()
        #p.start = start
        #print(p)

        s = SPath()     #startknoten erzeugen
        s.start = None
        s.target = start
        s.weight = 0
        vorgang_weight = 0     # vorgänger weight für nächsten knoten
        besucht.append(s)  # ersten knoten hinzufügen
        vorgang_start = start
        vorgang_dir = None
        route: Optional[List[Tuple[Tuple[int, int], Direction]]]
        route = []  # Optional[List[Tuple[Tuple[int, int], Direction]]]
        shp_list = []
        start_shp = None
        i = 1
        try:
            while True:
                print(f"start:  {start}")
                print(f"target: {target}")

                for tupel in self.planetPaths[start].items():  # arbeitliste mit benachbarten knoten füllen
                    print("lookup: ")
                    pprint.pprint(self.planetPaths[start])

                    if not (any(p.start == tupel[1][0] for p in besucht) and (vorgang_weight + tupel[1][2] > tupel[1][2])) and tupel[1][2] >= 0: #not(target einer der besuchten p.start and weight.route grösser als weight knoten)
                        p = SPath()
                        p.start = start
                        p.target = tupel[1][0]
                        p.direction = tupel[0]
                        print(f"prev weight: {vorgang_weight}")
                        print(f"current weight: {tupel[1][2]}")
                        p.weight = vorgang_weight + tupel[1][2]   # weight aus vorgänger addieren

                        #p.path.append((vorgang_start, vorgang_dir))

                        besucht.append(p)
                        print(f"p.weight: {p.weight}")
                        print(f"p.start: {p.start}")
                        print(f"p.target: {p.target}")


                        aListe.append(p)
                        print(f"appended: {p}")     #TODO fügt möglichweise gleiches element 2 mal hinzu
                        print("-----------")

                    print("aListe: ")
                    pprint.pprint(aListe)

                minimum = min(aListe, key=lambda p: p.weight)   # minimum weight in der arbeitsliste finden
                print(f"!target: {minimum}")
                print("minimum: ")
                print(minimum.weight)
                # speichern und neues setup

                print(f"route from: {minimum.start}")

                pprint.pprint(self.planetPaths[minimum.start])
                print(minimum.target)
                # TODO fehler in diesem block
                '''
                for tupel in self.planetPaths[minimum.start].items():  # direction des minimums finden      #TODO finden der pfades, der als start minimum.start hat
                    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    print(f"tupel prüfen: {tupel}")
                    if tupel[1][0] == minimum.target:   # wenn target im eintrag gefunden
                        kleinstes = min(self.planetPaths[minimum.start].items(), key=lambda tupel: tupel[1][2])
                        print("__target stimmt__")
                        print(tupel)
                        print(f"kleinstes[1][2]: {kleinstes[1][2]}")
                        print(f"tupel[1][2]: {tupel[1][2]}")
                        if tupel[1][2] == kleinstes[1][2]:    # wenn auch kleinstes weight ist  #TODO hie ist der fehler: ist das richtige aber nicht kleinstes weight
                            minimum.direction = tupel[0]  # .value  #TODO value als grad zahl
                            print("set direction...")
                            print(f"minimum.direction: {minimum.direction}")
                        else:
                            print("keine direction hinzugefügt")
                    else:
                        print("target falsch")
                        #break
                '''


                print("__completed direction check__")
                print("minimum.target: ")
                print(minimum.target)
                print(f"!minimum.weight: {minimum.weight}")
                # route bilden
                r = SPath()
                r.start = minimum.start
                r.direction = minimum.direction     #TODO falsch
                r.target = minimum.target
                r.weight = minimum.weight
                route.append(r)
                #route.append((vorgang_start, vorgang_dir, minimum.target, minimum.weight))

                vorgang_weight = minimum.weight
                vorgang_start = minimum.start
                # vorgang_dir: Direction



                print("route: ")
                pprint.pprint(route)
                for v in route:
                    print(v.start, v.direction, v.target, v.weight)
                print("=========================")
                #aListe.clear()
                aListe.remove(minimum)

                start = minimum.target
                print(f"start:  {start}")
                print(f"target: {target}")
                print(f"--- new cycle ---{i}")
                i += 1
                if start == target:     # TODO: unittest
                    break
                if len(aListe) == 0:
                    return []

            # shp_list
            print("ROUTE")
            for v in route:

                print(v.start, v.direction, v.target, v.weight)

            while True:
                print("true")
                #print(route)
                print(f"target: {target}")

                #next((r for r in route if r.target == target), None)
                #path = next(filter(lambda r: r.target == target, route))
                #shp_list.append((r.start, r.direction))
                #target = r.start
                print(shp_list)

                for path in route:
                    print(f"pathstart: {path.start}")
                    if path.target == target:
                        print("append: ")

                        shp_list.append((path.start, path.direction.value))

                        target = path.start
                        print(shp_list)
                        print(target)
                        break

                print(start_save)
                if target == start_save:
                    break

            print("return")
            pprint.pprint(shp_list[::-1])   #reversed list
            return shp_list[::-1]
        except:
            return []

    def possible_directions(punkt: Tuple[int, int], Directions: List[Direction]):
        # checken, dass alle richtungen eingetragen
        pass
