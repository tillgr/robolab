#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict
import pprint
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


    def __init__(self):
        self.weight = None
        self.start = None #Tuple[int, int]
        self.target = None #Tuple[int, int]
        self.weight = None #int
        self.path = [] #List[Tuple[Tuple[int, int], Direction]]


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


    def direction_invert(self, direction):
        if direction == Direction.NORTH:
            return Direction.SOUTH
        if direction == Direction.EAST:
            return Direction.WEST
        if direction == Direction.SOUTH:
            return Direction.NORTH
        if direction == Direction.WEST:
            return Direction.EAST

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

        besucht = []
        aListe = []     #arbeitsliste

        #p = SPath()
        #p.start = start
        #print(p)

        s = SPath()     #startknoten erzeugen
        s.start = None
        s.target = start
        s.weight = 0
        vorgang = 0     # vorgänger weight für nächsten knoten
        besucht.append(s)  # ersten knoten hinzufügen
        vorgang_start = start
        vorgang_dir: Direction
        shp_route: Optional[List[Tuple[Tuple[int, int], Direction]]]
        shp_route = [] # Optional[List[Tuple[Tuple[int, int], Direction]]]

        while True:
            print(f"start:  {start}")
            print(f"target: {target}")


            for tupel in self.planetPaths[start].items():  # arbeitliste mit benachbarten knoten füllen
                print("lookup: ")
                pprint.pprint(self.planetPaths[start])
                if not any(p.start == tupel[1][0] for p in besucht): #target not einer der besuchten p.start
                    p = SPath()
                    p.start = start
                    p.target = tupel[1][0]
                    p.weight = vorgang + tupel[1][2]   # weight aus vorgänger addieren

                    #p.path.append((vorgang_start, vorgang_dir))

                    besucht.append(p)
                    print(f"p.weight: {p.weight}")
                    print(f"p.start: {p.start}")
                    print(f"p.target: {p.target}")
                    print("------------")

                    aListe.append(p)
                print("aListe: ")
                pprint.pprint(aListe)

            minimum = min(aListe, key=lambda p: p.weight)   # minimum weight in der arbeitsliste finden
            print(f"!target: {minimum}")
            print("minimum: ")
            print(minimum.weight)
            # speichern und neues setup
            start = minimum.target
            vorgang = minimum.weight
            vorgang_start = minimum.start
            #vorgang_dir: Direction

            for tupel in self.planetPaths[vorgang_start].items():
                if tupel[1][0] == minimum.target:
                    vorgang_dir = tupel[0]

            if start == target:
                break
            print("minimum.target: ")
            print(minimum.target)
            minimum.path.append((vorgang_start, vorgang_dir))
            shp_route.append(minimum)
            aListe.clear()

            print("shp_route: ")
            pprint.pprint(shp_route)

            print(f"start:  {start}")
            print(f"target: {target}")
            print("--- new cycle ---")
        return shp_route

    def possible_directions(punkt: Tuple[int, int], Directions: List[Direction]):
        # checken, dass alle richtungen eingetragen
        pass
