#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:00:39 2020

@author: marc
"""

import numpy as np
    
filename = "input-day3"

class TobboganJourney:
    
    def __init__(self, filename):   
        self.themap = np.array([], dtype=bool)
        self.journeylist = []
        self.readMapFromFile(filename)


    def readMapFromFile(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.themap = np.zeros([len(lines), len(lines[0])-1], dtype=bool)
            
            for i, l in enumerate(lines):
                for j, c in enumerate(l[:-1]):
                    if (c == '#'):
                        self.themap[i,j] = '#'
        
        
    def printmap(self):
        journeyListIter = iter(self.journeylist)
        jl = next(journeyListIter)
        for i in range(self.themap.shape[0]):
            for j in range(self.themap.shape[1]):
                if (jl[0] == i and jl[1] == j):
                    try:
                        print('X' if jl[2] else 'O', sep='', end='')
                        jl = next(journeyListIter)
                    except StopIteration:
                        print('#' if self.themap[i,j] else '.', sep='', end='')
                else:
                    print('#' if self.themap[i,j] else '.', sep='', end='')
            print('\n', sep='', end='')
        
        
    def tracemap(self, right, down):
        # Trace map along given path
        self.journeylist = []
        treesAlongRoute = 0
        line = 0
        col = 0
        
        for i in range(0, self.themap.shape[0], down):
            if (self.themap[line, col] == True):
                treesAlongRoute += 1    
                self.journeylist.append([line,col,True])
            else:
                self.journeylist.append([line,col,False])
            line += down
            col = (col + right) % self.themap.shape[1]
            
            
        return treesAlongRoute
    

tj = TobboganJourney(filename)
#tj.printmap()

#tj.printmap()
#tj.tracemap(1,2)
#tj.printmap()

productOfTraversals = tj.tracemap(1,1) * tj.tracemap(3,1) * tj.tracemap(5,1) * tj.tracemap(7,1) * tj.tracemap(1,2)

print("Task 1: Tracing with right=3, down=1: Hit", tj.tracemap(3,1), "trees!")
print("Task 2: Hit", productOfTraversals, "trees in total!")
    
#    def __main__(filename):
#        tj = TobboganJourney(filename)
#        #tj.printmap()
#        print("Task 1: Tracing with right=3, down=1: Hit", tj.tracemap(3,1), "trees!")
#        sumOfTraversals = tj.tracemap(1,1) + tj.tracemap(3,1) + tj.tracemap(5,1) + tj.tracemap(7,1) + tj.tracemap(1,2)
#        print("Task 2: Hit", sumOfTraversals, "trees in total!")
        
        

#if __name__ == '__main__':
#    TobboganJourney.__main__(filename)        