#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters
import math

class Odometry():
    r = 2.5         # Radius Räder
    a = 0           # Radabstand
    dx = 0          # Streckendifferenz
    dy = 0
    dl = 0          # zurückgelegte Strecke des linken Rads
    dr = 0
    s = 0           # zurückgelegte Strecke
    #gamma = Blickrichtung

    def position(self, gamma):
        alpha = (self.dl + self.dr)/self.a
        s = (self.dr + self.dl)/alpha * math.sin(alpha/2)

        dx = - math.sin(gamma + (alpha/2)) * s
        dy = math.cos(gamma + (alpha/2)) * s

        gamma += alpha

        # take list of [gamma, dl, dr]s and start position
        # return calculated position
