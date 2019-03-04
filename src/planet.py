#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict, Any

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


class Planet:  # Karte
    """
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.planetKarte = []
        self.planetPaths = {}
        self.paths = {}
        self.target = None

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):  # Koordinaten, Hin/Rückrichtung

        self.planetKarte.append([start, target, weight])

        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it
        example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """

        pass

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        ''' [[((0, 0), < Direction.NORTH: 0 >), ((0, 1), < Direction.SOUTH: 180 >), 1]
            [((0, 0), <Direction.EAST: 90>), ((1, 0), <Direction.WEST: 270>), 1]'''

        for i in range(0, len(self.planetKarte)):  # vergleicht Elemente (Knoten) der Liste planetPaths (a, b)
            a = self.planetKarte[i][0][0]
            c = self.planetKarte[i][1][0]
            for j in range(1, len(self.planetKarte)):
                b = self.planetKarte[j][0][0]
                d = self.planetKarte[j][1][0]
                w = self.planetKarte[j][2]  # w ist wichtung der kanten

                if a == b:  # bei Pfaden mit gleichen Startknoten: eintragen in Dict: {a: {richtung von a: [b, richtung von b, wichtung]}}
                    self.planetPaths[a] = self.paths
                    self.paths[self.planetKarte[i][0][1]] = [b, self.planetKarte[j][1][1], w]

                if c == d:
                    self.planetPaths[c] = self.paths
                    self.paths[self.planetKarte[i][0][1]] = [d, self.planetKarte[j][1][1], w]

                if a == d:
                    self.planetPaths[a] = self.paths
                    self.paths[self.planetKarte[i][0][1]] = [d, self.planetKarte[j][1][1], w]

                if c == b:
                    self.planetPaths[c] = self.paths
                    self.paths[self.planetKarte[i][0][1]] = [b, self.planetKarte[j][1][1], w]


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
        return self.planetPaths

        pass

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[
        List[Tuple[Tuple[int, int], Direction]]]: #ausgabewert


        """
        Returns a shortest path between two nodes
        examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: List, Direction
        """
        pass
