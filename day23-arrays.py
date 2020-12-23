#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 06:15:01 2020

@author: marc
"""

import numpy as np

#inp = "284573961"
inp = "389125467"

cups = np.array([int(i) for i in inp])
pos  = np.array(list(range(len(cups)))) # pos[initialidx] = position of cup cupnr in current state
                                        # cups[pos[5]] is cup with original index 5 in current state 
nrmoves = 100
curidx = 0
npick = 3 # number of cups to pick up
ncups = len(cups)
#pickup = []

for i in range(nrmoves):
    curcup = cups[curidx]
    pickfrom = (curidx+1) % ncups
    pickup = []
    removedIdcs = []
    for j in range(npick):
        pickidx = (pickfrom+j) % ncups
        removedIdcs.append(pickidx)
        pickup.append(cups[pos[pickidx]])
        if pickidx < curidx:
            curidx -= 1
    print(cups)
    print(pickup)
    dest = curcup - 1
    while (dest in pickup) or (dest == 0):
        if dest == 0:
            dest = ncups
        else:
            dest -= 1
    destidx = pos[np.where(cups == dest)[0][0]] #cups.index(dest)
    print(dest); print()
    if destidx < curidx:
        curidx = curidx + npick 
#    for p in pickup[::-1]:
#        cups.insert(destidx+1, p)
    tmp = pos[destidx:destidx+npick]
    pos[destidx:destidx+npick] = pickup
    tmp2 = pos[-3:]
    pos[destidx+npick:] = np.hstack((tmp, pos[destidx+npick:-3]))
    curidx = (curidx+1) % ncups
    
print(cups); print()

output = ""
for c in cups:
    output += str(c)
output = output[output.index('1')+1:] + output[:output.index('1')]

print(output)