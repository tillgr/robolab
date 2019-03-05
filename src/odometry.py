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
        self.gamma = (gamma/180)*math.pi
        print(self.gamma)

        i=0

        for dist in listDistances:
            self.dl = dist[0]
            self.dr = dist[1]

            alpha = (self.dl - self.dr)/self.a

            #print(f"alpha: {alpha}")
            #s = 2 * self.r * math.sin(alpha/2)

            if self.gamma < 0:
                self.gamma = 2*math.pi + self.gamma
            elif self.gamma > 2*math.pi:
                self.gamma -= 2*math.pi

            if alpha == 0.0:
                if (0 < self.gamma < (45 / 180) * math.pi) or ((315 / 180) * math.pi < self.gamma < (359 / 180) * math.pi):
                    self.dY += self.dr/50
                elif (45 / 180)*math.pi < self.gamma < (135 / 180)*math.pi:
                    self.dX += self.dr/50
                elif (135/180)*math.pi < self.gamma < (225/180)*math.pi:
                    self.dY -= self.dr/50
                elif (225/180)*math.pi < self.gamma < (315/180)*math.pi:
                    self.dX -= self.dr/50
            else:

                #s = 2 * self.r * math.sin(alpha / 2)
                s = ((self.dr + self.dl) / alpha) * math.sin(alpha / 2)

                self.dX -= math.sin(self.gamma + (alpha/2)) * s
                self.dY += math.cos(self.gamma + (alpha/2)) * s

            self.gamma += alpha


        Xe = Xs + self.dX
        Ye = Ys + self.dY

        print(f"x: {Xe}")
        print(f"y: {Ye}")
        print(f"direction: {(self.gamma*180)/math.pi}")

        # return calculated position and direction
