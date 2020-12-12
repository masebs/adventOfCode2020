#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 05:52:17 2020

@author: marc
"""

import numpy as np

class shipTrace():
    def __init__(self, filename):
        with open(filename, 'r') as f:
            lines = list(f.read().splitlines())
        self.pos = np.array([0,0]) # current position
        self.d = np.array([1,0])   # current direction: [1,0] = E, [-1,0] = W, [0,1] = N, [0,-1] = S
        self.cmds = [[lines[i][0], int(lines[i][1:])] for i in range(len(lines))]

    def getDir(self,cmd):
        dirs = np.array([[0,1], [1,0], [0,-1], [-1,0]])
        if (cmd[0] == 'N'):
            return cmd[1]*np.array([0,1])
        elif (cmd[0] == 'E'):
            return cmd[1]*np.array([1,0])
        elif (cmd[0] == 'S'):
            return cmd[1]*np.array([0,-1])
        elif (cmd[0] == 'W'):
            return cmd[1]*np.array([-1,0])
        elif (cmd[0] == 'L'):
            if (cmd[1] % 90 != 0):
                print(f"WARNING: Ship can only steer along coordinate axes! Using {cmd[1] // 90} instead of {cmd[1]}")
            self.d = dirs[(np.where((dirs[:] == self.d).all(axis=1))[0][0] - cmd[1] // 90) % len(dirs)]
            return np.array([0,0])
        elif (cmd[0] == 'R'):
            if (cmd[1] % 90 != 0):
                print(f"WARNING: Ship can only steer along coordinate axes! Using {cmd[1] // 90} instead of {cmd[1]}")
            self.d = dirs[(np.where((dirs[:] == self.d).all(axis=1))[0][0] + cmd[1] // 90) % len(dirs)]
            return np.array([0,0])
        elif (cmd[0] == 'F'):
            return self.d * cmd[1]
        else:
            print("WARNING: Invalid command found")
            return None
        
    def traceShip(self):
        distTravelled = 0
        startpos = np.copy(self.pos)
        for i, c in enumerate(self.cmds):
            oldpos = np.copy(self.pos)
            self.pos += self.getDir(c) 
            distTravelled += np.sum(np.abs(self.pos - oldpos))
        distFromStart = np.sum(np.abs(self.pos - startpos))
        print(f"Task 1: Finished tracing ship. Distance travelled: {distTravelled}, final position: {self.pos}, Manhattan distance from start: {distFromStart}")
     
st = shipTrace("input-day12")
st.traceShip()
