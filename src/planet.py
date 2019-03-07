#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict



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
        # print(f"Start: {start}")

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
            if start[0] in self.planetPaths:        # wenn knoten in dict, richtung adden
                self.paths.update({start[0]:(target[0], target[1], weight)})
            else:
                self.paths = {start[1] : (target[0], target[1], weight)}        # ansonsten neuen key anlegen
                self.planetPaths.update({start[0]: self.paths})         # richtung adden

            # TODO richtung invertieren, der rückweg


            if target[0] in self.planetPaths:
                self.paths.update({target[0]:(start[0], start[1], weight)})
            else:
                self.paths = {target[1] : (start[0], start[1], weight)}
                self.planetPaths.update({target[0]: self.paths})






        """ a = self.planetKarte[i][0][0]
            c = self.planetKarte[i][1][0]
        
            b = self.planetKarte[j][0][0]
                d = self.planetKarte[j][1][0]
                w = self.planetKarte[j][2]  # w ist wichtung der kanten
        """

        """

                    
        for i in range(0, len(self.planetKarte)-1):  # vergleicht Elemente (Knoten) der Liste planetPaths (a, b)

            for j in range(1, len(self.planetKarte)-1): # TODO: wie funktioniert range in kombination mit len


                # TODO mehrere sachen hinzufügen möglich? neuer eintrag erzeugt, wenn key nicht vorhand?

                if a == b:  # bei Pfaden mit gleichen Startknoten: eintragen in Dict: {a: {richtung von a: [b, richtung von b, wichtung]}}
                    self.paths[self.planetKarte[i][0][1]] = [b, self.planetKarte[j][1][1], w]
                    self.planetPaths[a] = self.paths

                if c == d:
                    self.paths[self.planetKarte[i][0][1]] = [d, self.planetKarte[j][1][1], w]
                    self.planetPaths[c] = self.paths

                if a == d:
                    self.paths[self.planetKarte[i][0][1]] = [d, self.planetKarte[j][1][1], w]
                    self.planetPaths[a] = self.paths

                if c == b:
                    self.paths[self.planetKarte[i][0][1]] = [b, self.planetKarte[j][1][1], w]
                    self.planetPaths[c] = self.paths
        """
        pass

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
        print(self.planetPaths.items())
        return self.planetPaths

        pass

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int])-> Optional[List[Tuple[Tuple[int, int], Direction]]]:

        """setup-----------------------------------------------------------------------------------------------------"""
        gewaehlt = []
        rkm = []        # randknoten von s allgemein: [line, line, line, ...], nachshlagewerk
        line = []

        # erstellt rkm liste
        for s,v, in self.planetPaths.items():
            for dir_s, v in self.planetPaths.get(s).items():
                weight = v[2]
                t = v[0]    # target
                line.append((t, dir_s, weight, s))
            rkm.append(line.copy())
            #print("line:")
            #print(line)
            line.clear()
            #print("rkm:")
            #print(rkm)

        """dijkstra--------------------------------------------------------------------------------------------------"""

        rkm_d = []    # rkm arbeitsliste
        line = []       #hilfszeile

        # print("rkm:")
        # print(rkm[1])
        for line in rkm:        # startknoten einfügen
            # print(f"test: {line}")
            for tupel in line:
                print(f"tupel: {tupel}")
                print(tupel[0])
                print("Start: ")
                # print(start)
                if tupel[0] == start:       # TODO wählt nicht aus #start
                    gewaehlt.append(tupel)
                print("gewaehlt: ")
                print(gewaehlt)
        i = 0

        while True:

            for line in rkm:        # nachbarknoten in rkm finden
                # line = []
                for tupel in line:
                    # print(gewaehlt[i][0])
                    print(tupel[3])
                    if gewaehlt[i][0] == tupel[3]:
                        tupel[2] = tupel[2] + gewaehlt[i][2]        # weight aktualisieren
                        line.append(tupel)
                    rkm_d.append(line)                  # einfügen in rkm_d
                    line.clear()
            if i>0:
                for i in range(0, len(rkm_d[i-1])):     #vorherige tupel übernehmen
                    if rkm_d[i - 1][i] not in gewaehlt:
                        line.append(rkm_d[i - 1][i])
                        line[2] = gewaehlt[i][2]        # weight aktualisieren
                rkm_d.append(line)
                line.clear()

            for i in range(0, len(rkm_d[i])):       #tupel mit kleinster weight finden  # TODO
                if min(rkm_d[i][2]):
                    gewaehlt.append(rkm_d[i])       # einfügen in gewählt
            i+=1

            if len(rkm_d[i]) is not 0:
                break
            print("rkm:")
            print(rkm_d)
            print(len(rkm_d[i]))
        """output----------------------------------------------------------------------------------------------------"""
        shp = []        # TODO richtung ist rückwärts
        index: int

        for tupel in gewaehlt:  # tupel in gewählt suchen
            for t, dir_s, weight, s in tupel:
                if t == target:
                    shp.append(tupel)
                    index = gewaehlt.index(tupel)       # index merken
        while index is not 0:
            for tupel in rkm_d[index-1]:        # eins zurück gehen
                for t, dir_s, weight, s in tupel:
                    if s == gewaehlt[index][3]:     # folgeknoten suchen
                        shp.append(tupel)
                        index -= 1
        print(rkm)

        shp_route = [(shp[-1], None)]  # route für roboter
        for j in range(len(shp)-1, 0):      # liste rückwerts durchgehen, route bilden
            shp_route.append((shp[i][3], shp[i+1][1]))



        """
        Returns a shortest path between two nodes
        examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: List, Direction
        """

        return shp_route
