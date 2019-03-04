#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters
import math


class Odometry:
    r = 2.6         # Radius Räder
    a = 12           # Radabstand
    dX = 0          # Streckendifferenz
    dY = 0
    dl = 0          # zurückgelegte Strecke des linken Rads
    dr = 0
    s = 0           # zurückgelegte Strecke
    gamma = 0       # Blickrichtung

    def position(self, gamma, Xs, Ys, listDistances):
        self.gamma = gamma

        for i in listDistances:
            #self.dl = list(i)[0]
            #self.dr = list(i)[1]

            #alpha = (self.dl + self.dr)/self.a
            alpha = listDistances(i)
            s = (self.dr + self.dl)/alpha * math.sin(alpha/2)

            self.dX += - math.sin(gamma + (alpha/2)) * s
            self.dY += math.cos(gamma + (alpha/2)) * s

            gamma += alpha


        Xe = Xs + self.dX
        Ye = Ys + self.dY

        print(f"x: {Xe}")
        print(f"y: {Ye}")

        # take list of [dl, dr]s, start position and
        # return calculated position and direction
