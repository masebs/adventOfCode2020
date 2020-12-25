#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 08:43:40 2020

@author: marc
"""

#inp = [5764801, 17807724] # test
inp = [5290733, 15231938] # actual

def findLoopsize(pubkey, subjectnr, maxtry):
    val = 1
    for i in range(1,maxtry):
        val *= subjectnr
        val = val % 20201227
        if val == pubkey:
            return i
        
def transform(subjectnr, loopsize):
    val = 1
    for i in range(loopsize):
        val *= subjectnr
        val = val % 20201227
    return val

loopsize = []
for i in range(len(inp)):
    loopsize.append(findLoopsize(inp[i], 7, 10000000))

print(f"Loopsizes are {loopsize}")

keys = []
for i in range(len(inp)):
    keys.append(transform(inp[i], loopsize[len(inp)-1-i]))
    
print(f"Task 1: They keys are {keys}.")
    
        