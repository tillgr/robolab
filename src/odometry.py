#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters
import math


class Odometry:
    r = 2.5         # Radius Räder
    a = 0           # Radabstand
    dX = 0          # Streckendifferenz
    dY = 0
    dl = 0          # zurückgelegte Strecke des linken Rads
    dr = 0
    s = 0           # zurückgelegte Strecke
    gamma = 0       # Blickrichtung

    def position(self, gamma, Xs, Ys):
        self.gamma = gamma

        # for loop to iterate through list
        alpha = (self.dl + self.dr)/self.a
        s = (self.dr + self.dl)/alpha * math.sin(alpha/2)

        dX = - math.sin(gamma + (alpha/2)) * s
        dY = math.cos(gamma + (alpha/2)) * s

        gamma += alpha


        Xe = Xs + dX
        Ye = Ys + dY

        # take list of [dl, dr]s, start position and
        # return calculated position and direction
