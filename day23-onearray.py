#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 06:15:01 2020

@author: marc
"""

import numpy as np

inp = "284573961"
# inp = "389125467"

ncups = 1000000
cups = [int(i) for i in inp]
cups += list(range(max(cups)+1, ncups+1))
cups = np.array(cups)
pos = list(range(-1, cups.shape[0]))
pos = np.array(pos) # cups[pos[cuplabel]] == cuplabel
for i in range(1,len(inp)+1):
    pos[i] = np.where(cups == i)[0][0]

nrmoves = 10000000
curidx = 0
npick = 3 # number of cups to pick up
ncups = len(cups)

for i in range(nrmoves):
    if i % 5000 == 0:
        print(f"move {i}...")
    curcup = cups[curidx]
    pickfrom = (curidx+1) % ncups
    pickidcs = []
    for j in range(npick):
        pickidx = (pickfrom+j) % ncups
        pickidcs.append(pickidx)
    
    minidx = min(pickidcs)
    maxidx = max(pickidcs)
    if pickidcs == list(range(minidx, maxidx+1)):
        pick = np.copy(cups[minidx:maxidx+1])
    else:
        picklist = []
        for p in pickidcs:
            picklist.append(cups[p])
        pick = np.array(picklist)
        
    dest = curcup - 1
    while (dest in pick) or (dest == 0):
        if dest == 0:
            dest = ncups
        else:
            dest -= 1    
    destidx = pos[dest] #np.where(cups == dest)[0][0]
    
    # if len(cups) < 20:
    #     print(cups)
    #     print(pick)
    #     print(curcup, dest)
    #     for i in range(1,ncups):
    #         if not cups[pos[i]] == i:
    #             print("WARNING: pos wrong")
    #             break
    #     if len(set(cups)) != len(cups):
    #         print("WARNING: Lost a number")
    
    if destidx < curidx:
        if curidx+1+npick < ncups:
            tmp = np.copy(cups[destidx+1:curidx+1])
            cups[destidx+1+npick:curidx+1+npick] = tmp
            pos[tmp] = list(range(destidx+1+npick,curidx+1+npick))
        else:
            tmp1 = cups[destidx+1:ncups]
            tmp2 = cups[:(curidx+1)%ncups]
            tmp = np.hstack((tmp1, tmp2))
            for j in range(destidx+1+npick, curidx+1+npick):
                cups[j%ncups] = tmp[j-(destidx+1+npick)]
                pos[tmp[j-(destidx+1+npick)]] = j%ncups
        if destidx+1+npick < ncups:
            cups[destidx+1:destidx+1+npick] = pick
            pos[pick] = list(range(destidx+1, destidx+1+npick))
        else:
            for j in range(destidx+1, destidx+1+npick):
                cups[j%ncups] = pick[j-(destidx+1)]
                pos[pick[j-(destidx+1)]] = j%ncups
        curidx = (curidx + npick) % ncups
    else:
        tmp = np.copy(cups[curidx+1+npick:destidx+1])
        cups[curidx+1:destidx+1-npick] = tmp
        pos[tmp] = list(range(curidx+1, destidx+1-npick))
        cups[destidx+1-npick:destidx+1] = pick
        pos[pick] = list(range(destidx+1-npick, destidx+1))
        
    curidx = (curidx + 1) % ncups

if len(cups) < 20:
    print(); print(cups); print()
    output = ""
    for c in cups:
        output += str(c)
    output = output[output.index('1')+1:] + output[:output.index('1')]
    print(output)

label1 = cups[pos[1]+1]
label2 = cups[pos[1]+2]

print(f"Task 2: Stars are under cups {label1} and {label2}. Product is {label1*label2}")