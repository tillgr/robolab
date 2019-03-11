#!/usr/bin/env python3

import unittest
from planet import Direction, Planet
import pprint


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        example planet:

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """

        # set your data structure
        self.planet = Planet()

        # add the paths
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)

    #def test_target_not_reachable_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is no shortest path
     #   self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class YourFirstTestPlanet(unittest.TestCase):
    def setUp(self):
        """

        Planet:

            +--+
            |  |
            +-0,3------+
               |       |
              0,2-----2,2 (target)
               |      /
            +-0,1    /
            |  |    /
            +-0,0-1,0
               |
            (start)

        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # set your data structure
        self.planet = Planet()

        # ADD YOUR PATHS HERE:
        # self.planet.add_path(...)
        '''
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        '''

    def test_add_paths(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        pprint.pprint(self.planet.planetKarte)

    def test_get_paths(self):
        self.planet.get_paths()
        pprint.pprint(self.planet.planetPaths)

        """
        print(sorted(self.planet.planetPaths))
        print(list(range(0,10)))

        l = [(1, 5),(2,5),(3,5)]

        for k,v in l:
            print(k, v)

        for s,v, in self.planet.planetPaths.items():
            print("!")
            print(s)
            #print(v)

            for k,v in self.planet.planetPaths.get(s).items():
                print(s, v[0], v[2])
                #print(v)
        """



    def test_integrity(self):
        # were all paths added correctly to the planet
        # check if add_path() works by using get_paths()
        self.assertEqual(self.planet.get_paths(),
        {(0, 0): {  Direction.NORTH : ((0, 1),  Direction.SOUTH , 1),
                     Direction.EAST : ((1, 0),  Direction.WEST , 1),
                     Direction.WEST : ((0, 1),  Direction.WEST , 2)},
        (0, 1): {  Direction.NORTH : ((0, 2),  Direction.SOUTH , 1),
                     Direction.SOUTH : ((0, 0),  Direction.NORTH , 1),
                     Direction.WEST : ((0, 0),  Direction.WEST , 2)},
        (0, 2): {  Direction.NORTH : ((0, 3),  Direction.SOUTH , 1),
                     Direction.EAST : ((2, 2),  Direction.WEST , 2),
                     Direction.SOUTH: ((0, 1),  Direction.NORTH, 1)},
        (0, 3): {  Direction.NORTH : ((0, 3),  Direction.WEST , 2),
                     Direction.EAST: ((2, 2),  Direction.NORTH , 3),
                     Direction.SOUTH : ((0, 2),  Direction.NORTH , 1),
                     Direction.WEST: ((0, 3),  Direction.NORTH , 2)},
        (1, 0): {  Direction.NORTH: ((2, 2),  Direction.SOUTH , 3),
                     Direction.WEST : ((0, 0),  Direction.EAST , 1)},
        (2, 2): {  Direction.NORTH : ((0, 3),  Direction.EAST , 3),
                     Direction.SOUTH : ((1, 0),  Direction.NORTH , 3),
                     Direction.WEST : ((0, 2),  Direction.EAST, 2)}})

        #self.fail('implement me!')


    def test_empty_planet(self):
        self.assertEqual(self.planet.shortest_path((0, 0), (1, 2)), [])


    def test_target_not_reachable(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        self.assertEqual(self.planet.shortest_path((0, 0), (1, 2)), [])
        #self.fail('implement me!')


    def test_shortest_path(self):
        # at least 2 possible paths
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 2)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        #self.planet.get_paths()
        self.assertEqual(self.planet.shortest_path((0, 0), (2, 2)), [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)])

        #print(self.planet.planetPaths.items())
        #self.fail('implement me!')


    def test_same_length(self):
        # at least 2 possible paths with the same weight
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 4)
        self.assertEqual(self.planet.shortest_path((0,0),(2,2,)), ([((0,0), 0), ((0,1), 0), ((0,2), 90)] or [((0,0), 90), ((1,0), 0)]))
        #self.fail('implement me!')

    def test_shortest_path_with_loop(self):
        # does the shortest path algorithm loop infinitely?
        # there is a shortest path
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 5)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        self.assertEqual(self.planet.shortest_path((0,2),(2,2,)), [((0,2), 0), ((0,3), 90)])
        #self.fail('implement me!')

    def test_target_not_reachable_with_loop(self):
        #there is no shortest path
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.EAST), ((1, 1), Direction.WEST), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((1, 0), Direction.EAST), 1)
        self.planet.add_path(((1, 0), Direction.NORTH), ((1,1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.NORTH), ((1,1), Direction.SOUTH), 2)
        self.planet.add_path(((0, 1), Direction.EAST), ((1, 0), Direction.WEST), 2)
        self.planet.add_path(((0,0), Direction.WEST), ((0,0), Direction.NORTH), 1)

        self.assertEqual(self.planet.shortest_path((0, 0), (5,5)), [])
        #self.fail('implement me!')

    def test_target_not_reacheable_blocked(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), -1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        #self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        #self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        self.assertEqual(self.planet.shortest_path((0, 0), (0,3)), [])

    def test_target_not_reacheable_blocked_with_loop(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), -1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)

        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 0), Direction.WEST), 1)
        # self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)
        self.assertEqual(self.planet.shortest_path((0, 0), (0, 3)), [])
        pass
    def test_shortest_path_with_blocked(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), -1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), -1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.EAST), ((2, 2), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 2)
        self.planet.add_path(((0, 3), Direction.EAST), ((2, 2), Direction.NORTH), 3)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 3)

        pass

    def test_add_path_twice(self):
        # at least 2 possible paths
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), -1)
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)

        self.assertEqual(self.planet.planetPaths, self.planet.get_paths())
        # self.planet.get_paths()
        print(self.planet.planetPaths)

    def test_add_path_bidirectional(self):
        self.planet.add_path(((0, 0), Direction.WEST), ((0, 1), Direction.WEST), 2)
        map_test = {(0,0):{Direction.WEST: ((0,1), Direction.WEST, 2)},
                    (0,1): {Direction.WEST: ((0,0), Direction.WEST, 2)}
                    }
        self.assertEqual(self.planet.get_paths(), map_test)
        pass


if __name__ == "__main__":
    unittest.main()
