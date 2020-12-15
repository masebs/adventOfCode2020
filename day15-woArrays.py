#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 06:00:31 2020

@author: marc
"""

#import numpy as np

inp = [6,3,15,13,1,0]
N = 30000000

curpos = len(inp)
curnr = inp[-1] #nrs[curpos-1]
oldnr = inp[-1]

# this is crucial: store positions in an array (or dictionary); otherwise we spend an eternity searching for them!
pos = {} # dictionary - less memory than array and equally fast

for k,i in enumerate(inp):  # write position of the initial elements
    pos[i] = [k,-1]   # for np.array or dict
    
for i in range(len(inp), N):
    p = pos[curnr]
    if (p[1] == -1): # spoken the first time
        curnr = 0
    else:
        curnr = p[0] - p[1] #lastoc[cidx] - seclastoc[cidx]
    
    if ((i+1) % 500000 == 0):
        print(f"Turn {i+1}: curnr = {curnr}")
        
    try:    
        p = pos[curnr]
        residx = p[0] # for dict
    except (KeyError):
        residx = -1
    
    if (residx != -1): # res is already present
        pos[curnr] = [i, p[0]] # add last mention of that number 
    else:               # res is not yet present
        pos[curnr] = [i, -1]  
    #print(curnr)
        
print(f"Task 1/2: The {N}th number spoken is {curnr}.")
    
    