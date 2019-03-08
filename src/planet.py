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
    def __init__(self):
        self.start: Tuple[int, int]
        self.target: Tuple[int, int]
        self.weight: int
        self.path: List[Tuple[Tuple[int, int], Direction]]


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

            # TODO richtung invertieren, der rückweg
            '''
            if target[0] not in self.planetPaths.keys():
                self.paths = {self.direction_invert(target[1]): (start[0], self.direction_invert(start[1]), weight)}
                self.planetPaths.update({target[0]: self.paths})
            else:
                self.planetPaths[target[0]].update({target[1]: (start[0], self.direction_invert(start[1]), weight)})
            '''
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

    def update_weight(self, tupel: Tuple[Direction, Tuple[Tuple[int, int], Direction, Weight]], new_value: int):
        lst = list(tupel)
        lst2 = list(lst[1])
        lst2[2] = new_value

        lst[1] = tuple(lst2)
        tupel = tuple(lst)
        # print(tupel)
        return tupel

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[
        List[Tuple[Tuple[int, int], Direction]]]:

        besucht = []
        aListe = []

        #p = SPath()
        #p.start = start
        #print(p)

        weights = []
        directions = []
        tupels = []

        s = SPath()
        s.start = start
        s.target = start
        s.weight = 0

        besucht.append(s)  # ersten knoten hinzufügen

        for tupel in self.planetPaths[start].items():  # arbeitliste mit benachbarten knoten füllen
            p = SPath()
            p.start = start
            p.target = tupel[1][0]
            p.weight = s.weight + tupel[1][2]

            if p not in besucht:
                aListe.append(p)

            print(f"target: {p.target}")
        pprint.pprint(aListe)



        for i in range(0, len(aListe)-1):       # minimum in der arbeitsliste finden
            minimum = aListe[i]
            print("liste: ")
            print(minimum.weight)
            for j in range(1, len(aListe)):
                if aListe[i].weight > aListe[j].weight:
                    minimum = aListe[j]
                    besucht.append(minimum)
                    print(f"minimum: {minimum}")



    '''
        besucht.append(target)
        # print(besucht)
        self.dijkstra = copy.deepcopy(self.planetPaths)
        pprint.pprint(self.dijkstra.items())
        # pprint.pprint(f"v{v}")
        # pprint.pprint(f"items: {v.items()}")

        #for tupel in self.dijkstra[target].items():  # weights und tupel extrahieren
            #self.tupels.append(tupel)
            #print("hello")
            #for v in self.tupels:    # weight aktualisieren, da am anfang 0
            #    self.update_weight(tupel, 0)
            #self.dijkstra[target] = self.tupels    # einfügen in planetPaths
        # TODO bis target gereacht schleife
        sum_weight = 0
        pprint.pprint(self.dijkstra.items())
        while target != start:

            for tupel in self.dijkstra[target].items():     # weights und tupel extrahieren
                if sum_weight < self.tupels[-1][1][2]:  # weight aktualisieren, wenn sum kleiner als jede weight des nachbarn
                    self.update_weight(tupel, sum_weight)      # weight aktualisieren

                self.tupels.append(tupel)       # extrahierte tupel

                self.weights.append(self.tupels[-1][1][2])      # extrahierte weights
                self.paths = {tupel[0]: (tupel[1][0], tupel[1][1], tupel[1][2])}    # neuen eintrag vorbereiten
                self.dijkstra[target] = self.paths     # einfügen in dijkstra

            for v in self.weights:
                if min(self.weights) == v:       # #kleinste weight finden
                    self.index = self.weights.index(v)
                    sum_weight = v    # weight in summe einfügen
                    print(f"index: {self.index}")
            for tupel in self.tupels:    # betreffendes tupel in besucht hinzufügen
                if self.tupels.index(tupel) == self.index:
                    besucht.append(tupel)
                    sum_weight += tupel[1][2]
                    target = tupel[1][0]      # neuen knoten finden   TODO: tupel[1][0], erzeugt endlosschleife
                    print(target)

            print(f"tupels: {self.tupels}")
            print(f"weights: {self.weights}")
            print(target)
            print(start)


        #return shp_route
    '''

    def possible_directions(punkt: Tuple[int, int], Directions: List[Direction]):
        # checken, dass alle richtungen eingetragen
        pass
