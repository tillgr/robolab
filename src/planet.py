#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict, Any

# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

planetKarte: List[Any] = []
planetPaths: Dict = []
paths: Dict = []

@unique
class Direction(IntEnum):           #Richtung
    """ Directions in degrees """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


# simple alias, no magic here
Weight = int                        #gewicht der kanten
""" 
    Weight of a given path (received from the server)
    value:  -1 if broken path 
            >0 for all other paths
            never 0
"""


class Planet:           #Karte
    """
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """



    def __init__(self):
        """ Initializes the data structure """
        self.target = None

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],         #Koordinaten, Hin/Rückrichtung
                 weight: int):


        planetKarte.append([start, target])

        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it
        example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        print(planetKarte)
        pass

    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:

        for i in range(0, len(planetKarte)):       #vergleicht Elemente (Knoten) der Liste planetPaths (a, b)
            a = planetKarte[i][1]
            for j in range(i+1, len(planetKarte)):
                b = planetKarte[j][1]
                w = planetKarte[j][3]               #w ist wichtung der kanten

                if a == b:                      #bei Pfaden mit gleichen Startknoten: eintragen in Dict: {a: {richtung von a: [b, richtung von b, wichtung]}}
                    {**planetPaths, a[1][1]: {**paths, a[1][2]: [b[1][1], b[1][2], w]}}

        return planetPaths

        print(planetPaths)



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
        pass

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:
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
