#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict
from collections import defaultdict


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
        self.dijk = {}  # dictionary für den dijkstra
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

        for i in range(0, len(self.planetKarte)-1):  # vergleicht Elemente (Knoten) der Liste planetPaths (a, b)
            a = self.planetKarte[i][0][0]
            c = self.planetKarte[i][1][0]
            for j in range(1, len(self.planetKarte)-1): # TODO: wie funktioniert range in kombination mit len
                b = self.planetKarte[j][0][0]
                d = self.planetKarte[j][1][0]
                w = self.planetKarte[j][2]  # w ist wichtung der kanten

                # TODO mehrere sachen hinzufügen möglich? neuer eintrag erzeugt, wenn key nicht vorhand?

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

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:  # ausgabewert

        s = start
        t = target
        gewaehlt = []
        i = 0

        rkm = self.planetPaths.get(s)  # randknotenmenge aus planetPaths
        self.dijk = {s: rkm.items()}  # eintrag in dijk s: rkm.items(), value ist typ liste # TODO welches format returnt .items?
        self.dijk = defaultdict(list)     # default datentyp für values von dijk ist list

        def update_dijkstra():
            gewaehlt.append(s)  # in gewählt hinzufügen

            last_key = sorted(self.dijk.keys())[-1]  # letzter key vor dem update aus dijk
            last_value = self.dijk[last_key]  # letzter wert des dijk vor update

            self.dijk[s] = rkm.items()  # nächste zeile anlegen mit neue nachbarknoten
            self.dijk[s].append(last_value)  # randknoten übernehmen

            if i > 0:
                self.dijk.get(s)[i][1][2] = self.dijk.get(s)[i - 1][1][2] + self.dijk.get(s)[i][1][2]  # in dijk weight updaten

            for k in range(0, len(self.dijk.get(s))-1):   # aktualisierung der knoten # TODO geht es um die anzahl oder die indizes? sonst endrange fixen
                a = self.dijk[s][k]    # element in s wählen
                a_w = self.dijk[s][k][0]    # width parameter von diesem element
                for l in range (1, len(self.dijk.get(s))-1):
                    b = self.dijk[s][l][0]
                    b_w = self.dijk[s][l][0]    # wird verglichen, zum aktualisieren
                    if a_w >= b_w:      # falls width größer/gleich, gelöscht
                        del a   # TODO aussage valide?
                    elif a_w < b_w:     # falls width kleiner gelöscht
                        del b
                    elif a_w < 0:       # falls broken: gelöscht
                        del a
                    elif b_w < 0:       # same here
                        del b

        while not len(self.planetPaths) == len(self.dijk):  # solange länge von planetPaths ungleich länge dijk
            for value in rkm.items():  # für richtungen von jeweiligen knoten aus
                if min(value[1][2]) and s not in gewaehlt:  # wenn minimum an weight in einem eintrag gefunden
                    # TODO, wie bestimmt man das minimum?
                    s = value  # s neu wählen # TODO wie läuft das mit dem scope?
                update_dijkstra()

        

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
