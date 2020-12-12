#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 05:46:55 2020

@author: marc
"""

import numpy as np

with open("input-day11", 'r') as f:
    lines = list(f.read().splitlines())

seats = np.zeros([len(lines), len(lines[0])], dtype=int)
for i, l in enumerate(lines):
    for j, c in enumerate(l):
        if (c == 'L'):
            seats[i,j] = 0
        elif (c == '.'):
            seats[i,j] = -1
        elif (c == '#'):
              seats[i,j] = 1
        else:
            print(f"WARNING: Invalid character in input at {i}, {j}")

def countNeighbours(seats):
    pass

counts = np.zeros(seats.shape)

print(seats)
changes = 1
while (changes > 0):
    changes = 0
    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            occup = 0
            for m in range(i-1,i+2):
                if (m < 0) or (m >= seats.shape[0]):
                    continue
                for n in range(j-1,j+2):
                    if (n < 0) or (n >= seats.shape[1]) or ((m == i) and (n == j)):
                        continue
                    if (seats[m,n] == 1):
                        occup += 1
                    #print(i,j,m,n, occup)
                    #seats[m,n] = -9
            counts[i,j] = occup
            
    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            if (seats[i,j] == 0) and (counts[i,j] == 0):
                seats[i,j] = 1
                changes += 1
            elif (seats[i,j] == 1) and (counts[i,j] >= 4):
                seats[i,j] = 0
                changes += 1     
    #print(counts)
    #print(seats)

occupSeats = np.where(seats == 1)[0].shape[0]

print(f"Task 1: There are {occupSeats} occupied seats.")
