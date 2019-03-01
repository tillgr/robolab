#!/usr/bin/env python3

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters
import math

class Odometry():
    r = 2.5         # Radius Räder
    dx = 0          # Streckendifferenz
    dy = 0
    dl = 0          # zurückgelegte Strecke des linken Rads
    dr = 0

