#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 06:15:01 2020

@author: marc
"""

#inp = "284573961"
inp = "389125467"

ncups = 1000000
cups = [int(i) for i in inp]
cups += list(range(max(cups)+1, ncups+1))

nrmoves = 10000000
curidx = 0
np = 3 # number of cups to pick up

for i in range(nrmoves):
    if i % 100 == 0:
        print(f"move {i}...")
#    print(cups)
    curcup = cups[curidx]
    pickfrom = (curidx+1) % ncups
#    pickup = []
    pickidcs = []
    for j in range(np):
        pickidx = (pickfrom+j) % ncups
        pickidcs.append(pickidx)
#        pickup.append(cups[pickidx])
        
    minidx = min(pickidcs)
    maxidx = max(pickidcs)
    if pickidcs == list(range(minidx, maxidx+1)):
        pick = cups[minidx:maxidx+1]
        del cups[minidx:maxidx+1]
        if maxidx < curidx:
            curidx -= np
    else:
        pick = [cups[i] for i in pickidcs]
        pickidcs.sort()
        for i in pickidcs[::-1]:
            del cups[i]
            if i < curidx:
                curidx -= 1
#    print(pick)

    dest = curcup - 1
    while dest not in cups:
        if dest == 0:
            dest = ncups
        else:
            dest -= 1
    destidx = cups.index(dest)
    if destidx < curidx:
        curidx = (curidx + np) % ncups
#    print(dest)
    
    cups[destidx+1:destidx+1] = pick
        
        #cups.insert(destidx, cups.pop(p))
#    print(curcup, curidx)
    curidx = (curidx+1) % ncups
#    print(curidx)
#    print()
    
print(cups); print()

output = ""
for c in cups:
    output += str(c)
output = output[output.index('1')+1:] + output[:output.index('1')]

print(output)