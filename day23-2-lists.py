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

#pickup = []

for i in range(nrmoves):
    if i % 100 == 0:
        print(f"move {i}...")
    curcup = cups[curidx]
    pickfrom = (curidx+1) % ncups
#    pickup = []
    pickidcs = []
    for j in range(np):
        pickidx = (pickfrom+j) % ncups
        pickidcs.append(pickidx)
#        pickup.append(cups.pop(pickidx)) # this is the slowest part
#        pickup.append(cups[pickidx])
        if pickidx < curidx:
            curidx -= 1
#    print(cups)
#    print(pickup)
#    for p in pickup:
#        cups.remove(p)
    dest = curcup - 1
    while dest not in cups:
        if dest == 0:
            dest = ncups
        else:
            dest -= 1
    destidx = cups.index(dest)
#    print(dest); print()
    if destidx < curidx:
        curidx = curidx + np 
#    cups = cups[:destidx] + pickup[::-1] + cups[destidx+1:]
    for p in pickidcs[::-1]:
        cups.insert(destidx+1, p)
    curidx = (curidx+1) % ncups
    
label1 = cups[cups.index(1)+1]
label2 = cups[cups.index(1)+2]

print(f"Task 2: Stars are under cups {label1} and {label2}. Product is {label1*label2}")