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


class Planet:  # Karte
    """
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """
    index = None
    sum_weight = 0

    def __init__(self):
        """ Initializes the data structure """
        self.planetKarte = []   # pfadpaare
        self.planetPaths = {}   # eigentliche karte
        self.paths = {}         # hile für einfügen in karte
        self.target = None      # routenziel
        self.weights = []       # hilfe für auswerten von karte
        self.tupels = []        # same
        self.dijkstra = {}     # kopie von karte für shp

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

        #print(self.planetKarte)
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
                self.paths = {start[1] : (target[0], target[1], weight)}        # ansonsten neuen key anlegen
                self.planetPaths.update({start[0]: self.paths})         # richtung adden
            else:        # wenn knoten in dict, richtung adden
                self.planetPaths[start[0]].update({start[1]:(target[0], target[1], weight)})
                #self.planetPaths.update({start[0] : self.paths})

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
        #print("karte")
        #pprint.pprint(self.planetKarte)
        #print("Paths")
        #pprint.pprint(self.planetPaths)

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
        #print(self.planetPaths.items())
        #print(self.planetPaths)
        return self.planetPaths

        pass

    def update_weight(self, tupel: Tuple[Direction, Tuple[Tuple[int, int], Direction, Weight]], new_value: int):
        lst = list(tupel)
        lst2 = list(lst[1])
        lst2[2] = new_value

        lst[1] = tuple(lst2)
        tupel = tuple(lst)
        #print(tupel)
        return tupel



    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int])-> Optional[List[Tuple[Tuple[int, int], Direction]]]:


        besucht = []

        besucht.append(target)
        #print(besucht)
        self.dijkstra = copy.deepcopy(self.planetPaths)
        pprint.pprint(self.dijkstra.items())
        #pprint.pprint(f"v{v}")
        #pprint.pprint(f"items: {v.items()}")

        for tupel in self.dijkstra[target].items():  # weights und tupel extrahieren
            self.tupels.append(tupel)
            print("hello")
            for v in self.tupels:    # weight aktualisieren, da am anfang 0
                self.update_weight(tupel, 0)
            self.planetPaths[target] = self.tupels    # einfügen in planetPaths
        # TODO bis target gereacht schleife
        pprint.pprint(self.dijkstra.items())
        # TODO v.items  nicht 2 mal benutzen

        for tupel in self.dijkstra[target].items():     # weights und tupel extrahieren
            self.tupels.append(tupel)
            if self.sum_weight < self.tupels[-1][1][2]:  # weight aktualisieren, wenn sum kleiner als jede weight des nachbarn
                self.update_weight(tupel, self.sum_weight)      #weight aktualisieren

            self.weights.append(self.tupels[-1][1][2])
            self.planetPaths[target] = self.tupels
            # TODO hier

        for v in self.weights:

            if min(self.weights) == v:       # #kleinste weight finden
                self.index = self.weights.index(v)
                self.sum_weight = v    # weight in summe einfügen
                print(self.index)
        for tupel in self.tupels:    # betreffendes tupel in besucht hinzufügen
            if self.tupels.index(tupel) == self.index:
                besucht.append(tupel)
                self.sum_weight += tupel[1][2]
                target = tupel[1][0]        # neuen knoten finden


        # TODO in planetPaths weight aktualisieren

        print(f"tupels: {self.tupels}")
        print(f"weights: {self.weights}")

        '''
        """setup-----------------------------------------------------------------------------------------------------"""
        gewaehlt = []
        rkm = []        # randknoten von s allgemein: [line, line, line, ...], nachshlagewerk
        line = []       # hilfszeile
        hilf =[]

        # erstellt rkm liste        # TODO hier ist der fehler: .items läuft nicht

        for s,v, in self.planetPaths.items():
            #print(f"items:{self.planetPaths.get(s).items()}\n")

            for v in self.planetPaths.get(s).items():        #dir_s
                #print(f"v:{v}\n")

                weight = v[1][2]
                t = v[1][0]    # target
                dir_s = v[0]
                line.append([t, dir_s, weight, s])          # TODO maybe statt line hilf verwenden
                #print(f"line: {line}\n")

            rkm.append(line.copy())

            line.clear()
            #print("rkm:")
            #print(rkm)
            #print("----")

        """dijkstra--------------------------------------------------------------------------------------------------"""

        rkm_d = []    # rkm arbeitsliste

        # print("rkm:")
        # print(rkm[1])
        for line in rkm:        # startknoten einfügen
            # print(f"test: {line}")
            for tupel in line:
                #print(f"tupel: {tupel}")
                ##print(tupel[0])
                ##print("Start: ")
                ##print(start)

                if tupel[0] == start:
                    gewaehlt.append(tupel)
                #print(f"hilf: {tupel}")
                #print("gewaehlt: ")
                #print(gewaehlt)

        i = 0
        #print("\nhier beginnt dijkstra :))\n")
        #print(rkm)
        while True:

            for line in rkm:        # nachbarknoten in rkm finden       # TODO endlosschleife
                for tupel in line:
                    # print(gewaehlt[i][0])
                    #print(f"tupel 3: {tupel[3]}")
                    if gewaehlt[i][0] == tupel[3] and tupel not in gewaehlt:        # t in tupel gewaehlt == s in tupel line rkm
                        print(f"gew: i: {gewaehlt[i][0]}")
                        hilf.append(tupel)
                        hilf[-1][2]= tupel[2] + gewaehlt[i][2]
                        # tupel[2] = tupel[2] + gewaehlt[i][2]        # weight aktualisieren # TODO unendlich oft einfügen
                        rkm_d.append(hilf.copy())                  # einfügen in rkm_d
                        print(f"append: {hilf}")
                        hilf.clear()
                print("break")
                #break
            if i>0:
                for v in range(0, len(rkm_d[i-1])):     #vorherige tupel übernehmen
                    if rkm_d[i - 1][v] not in gewaehlt:
                        hilf.append(rkm_d[i - 1][v])
                        hilf[-1][2] = gewaehlt[i][2]        # weight aktualisieren
                rkm_d.append(hilf.copy())
                hilf.clear()


            #print(f"länge: {len(rkm_d[i])}")

            #print("rkm:")
            #print(rkm_d)

            if len(rkm_d[i]) is 0:

                break

            #print(f"rkm_d: {rkm_d}")
            minimum = rkm_d[i][0][2]
            for tupel in rkm_d[i]:       #tupel mit kleinster weight finden
                #print(f"rkm_di: {rkm_d[i]}")
                #print(f"mini: {minimum}")
                #print(f"tupel[2]: {tupel[2]}")
                if tupel[2] < minimum:
                    minimum = tupel[2]
                    gewaehlt.append(tupel)       # einfügen in gewählt
                else:
                    gewaehlt.append(rkm_d[i][0])
                    # print("hi")
            i= i+ 1

            print(i)


        """output----------------------------------------------------------------------------------------------------"""
        shp = []        # TODO richtung ist rückwärts
        index: int

        for tupel in gewaehlt:  # tupel in gewählt suchen
            print(f"gewaehlt: {gewaehlt}")       # TODO komische tupel in gewählt
            #print("\n")
            print(tupel)

            if tupel[0] == target:      # TODO target befindet sich nicht in gewaehlt    #target
                shp.append(tupel)
                print("hi")
                index = gewaehlt.index(tupel)       # index merken
                print(index)

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


        '''
        """
        Returns a shortest path between two nodes
        examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: List, Direction
        """

        #return shp_route

    def possible_directions (punkt: Tuple[int, int], Directions: List[Direction]):
        # checken, dass alle richtungen eingetragen
        pass