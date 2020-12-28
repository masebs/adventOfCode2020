#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 05:58:54 2020

@author: marc
"""

with open("input-day9", 'r') as f:
    nr = list(map(int, f.read().splitlines()))

preamblelength = 25

# Laufzeit ca 100 ms
for i in range(preamblelength, len(nr)):      # O(n)
    isSum = False
    for j in range(i-preamblelength, i):      # O(1) (obwohl groß)
        for k in range(i-preamblelength, i):  # O(1)
            if (j != k):
                #print(f"Check {nr[i]} == {nr[j]} + {nr[k]}")
                if (nr[i] == nr[j] + nr[k]):
                    isSum = True
                    #print(f"  FOUND {nr[i]} == {nr[j]} + {nr[k]}")
    if not isSum: # found the first one, we don't look for more
        break
   
print(f"Task 1: First nr which does not obey to rule is line {i+1}: {nr[i]}")

iNr = nr[i]
iIdx = i
rangefrom = -1
rangeto = -1
found = False

# Laufzeit nur (!) ca 40 ms
for i in range(0, iIdx):       # O(n) (aber nur bis iIdx)
    s = 0
    for j in range(i, iIdx):   # O(n) (aber kleiner werdend und oft früh abgerbrochen)
       s += nr[j] 
       if (s > iNr):
           break
       if (s == iNr):
           found = True
           rangefrom = i
           rangeto = j
           break
           
minFromRange = min(nr[rangefrom:rangeto+1])
maxFromRange = max(nr[rangefrom:rangeto+1])
sumMinMax = minFromRange + maxFromRange

print(f"""Task 2: Invalid nr {iNr} is sum from lines {rangefrom+1} to {rangeto+1} (numbers {nr[rangefrom]} to {nr[rangeto]}). 
        Min and Max in this range are {minFromRange}, {maxFromRange}, and their sum is {sumMinMax}""")