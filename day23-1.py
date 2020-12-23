#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 06:15:01 2020

@author: marc
"""

inp = "284573961"
#inp = "389125467"

cups = [int(i) for i in inp]

nrmoves = 100
curidx = 0
np = 3 # number of cups to pick up
ncups = len(cups)
#pickup = []

for i in range(nrmoves):
    curcup = cups[curidx]
    pickfrom = (curidx+1) % ncups
    pickup = []
    for j in range(np):
        pickidx = (pickfrom+j) % ncups
        pickup.append(cups[pickidx])
        if pickidx < curidx:
            curidx -= 1
    print(cups)
    print(pickup)
    for p in pickup:
        cups.remove(p)
    dest = curcup - 1
    while dest not in cups:
        if dest == 0:
            dest = ncups
        else:
            dest -= 1
    destidx = cups.index(dest)
    print(dest); print()
    if destidx < curidx:
        curidx = curidx + np 
    for p in pickup[::-1]:
        cups.insert(destidx+1, p)
    curidx = (curidx+1) % ncups
    
print(cups); print()

output = ""
for c in cups:
    output += str(c)
output = output[output.index('1')+1:] + output[:output.index('1')]

print(output)