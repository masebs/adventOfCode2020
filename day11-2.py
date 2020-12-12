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

def getDirections(i,j, shape):
    dirlist = []
    d = []
    for m in range(i-1, -1, -1):     # vertical up
        d.append([m,j])
    dirlist.append(d)
    d = []
    for m in range(i+1, shape[0]):  # vertical down
        d.append([m,j])
    dirlist.append(d)
    d = []
    for m in range(j-1, -1, -1):
        d.append([i,m])       # horizontal left
    dirlist.append(d)
    d = []
    for m in range(j+1, shape[1]):
        d.append([i,m])       # horizontal right
    dirlist.append(d)
    d = []
    for m in range(i+1, shape[0]): 
        if not(j-(m-i) < 0) and not(j-(m-i) >= shape[1]):
            d.append([m,j-(m-i)])   # diagonal down left
    dirlist.append(d)
    d = []
    for m in range(i-1, -1, -1):
        if not(j-(m-i) < 0) and not(j-(m-i) >= shape[1]):
            d.append([m,j-(m-i)])   # diagonal up right
    dirlist.append(d)
    d = []
    for m in range(j+1, shape[1]):  
        if not (i+(m-j) < 0) and not(i+(m-j) >= shape[0]):
            d.append([i+(m-j),m])   # diagonal down right
    dirlist.append(d)
    d = []
    for m in range(j-1, -1, -1):  
        if not (i+(m-j) < 0) and not(i+(m-j) >= shape[0]):
            d.append([i+(m-j),m])   # diagonal up left
    dirlist.append(d)
    return dirlist

#print(getDirections(4,0,[5,5]))

counts = np.zeros(seats.shape)

print(seats)
changes = 1
count = 0
while (changes > 0):
    changes = 0
    count += 1
    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            occup = 0
            dirlist = getDirections(i, j, seats.shape)
            #print(dirlist)
            for d in dirlist:
                for n in d:
                    if (seats[n[0], n[1]] == 1):
                        occup += 1
                        break
                    if (seats[n[0], n[1]] == 0):
                        break
            counts[i,j] = occup
            
    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            if (seats[i,j] == 0) and (counts[i,j] == 0):
                seats[i,j] = 1
                changes += 1
            elif (seats[i,j] == 1) and (counts[i,j] >= 5):
                seats[i,j] = 0
                changes += 1     
    print(counts)
    print(seats)

occupSeats = np.where(seats == 1)[0].shape[0]

print(f"Task 2: There are {occupSeats} occupied seats. Done {count} cycles.")
