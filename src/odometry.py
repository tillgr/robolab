#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters
import math


class Odometry:
    x = 0
    y = 0
    r = 2.6         # Radius Räder
    a = 12          # Radabstand
    dX = 0          # Streckendifferenz
    dY = 0
    gamma = 0

    def get_position(self):
        return self.x, self.y

    def get_direction(self):
        return self.gamma

    def position(self, gamma, Xs, Ys, listDistances):
        self.dX = 0
        self.dY = 0

        if gamma == 90:
            self.gamma = (270 / 180) * math.pi
        elif gamma == 270:
            self.gamma = (90 / 180) * math.pi
        else:
            self.gamma = (gamma/180)*math.pi

        for dist in listDistances:
            self.dl = dist[0]
            self.dr = dist[1]

            alpha = (self.dr - self.dl)/self.a

            if self.gamma < 0:
                self.gamma += 2*math.pi
            elif self.gamma > 2*math.pi:
                self.gamma -= 2*math.pi

            if alpha == 0.0:
                if (0 < self.gamma < (45 / 180) * math.pi) or ((315 / 180) * math.pi < self.gamma < (359 / 180) * math.pi):
                    self.dY += self.dr/50
                elif (45 / 180)*math.pi < self.gamma < (135 / 180)*math.pi:
                    self.dX -= self.dr/50
                elif (135/180)*math.pi < self.gamma < (225/180)*math.pi:
                    self.dY -= self.dr/50
                elif (225/180)*math.pi < self.gamma < (315/180)*math.pi:
                    self.dX += self.dr/50
            else:
                s = (((self.dr + self.dl) / alpha) * math.sin(alpha / 2)) / 50

                self.dX -= math.sin(self.gamma + (alpha/2)) * s
                self.dY += math.cos(self.gamma + (alpha/2)) * s

            self.gamma += alpha

        Xe = Xs + round(self.dX)
        Ye = Ys + round(self.dY)

        self.x = Xe
        self.y = Ye

        print(f"x: {Xe}")
        print(f"y: {Ye}")

        #print(f"direction_raw: {self.gamma*180/math.pi}")

        if (0 < self.gamma < (45 / 180) * math.pi) or ((315 / 180) * math.pi < self.gamma < (359 / 180) * math.pi):
            self.gamma = 0
            print(f"direction: {0}")
        elif (45 / 180) * math.pi < self.gamma < (135 / 180) * math.pi:
            self.gamma = 270
            print(f"direction: {270}")
        elif (135 / 180) * math.pi < self.gamma < (225 / 180) * math.pi:
            self.gamma = 180
            print(f"direction: {180}")
        elif (225 / 180) * math.pi < self.gamma < (315 / 180) * math.pi:
            self.gamma = 90
            print(f"direction: {90}")
