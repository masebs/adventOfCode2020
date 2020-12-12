#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 05:42:22 2020

@author: marc
"""

with open("input-day10", 'r') as f:
    nr = list(map(int, f.read().splitlines()))

nr.append(0) # socket joltage
nr.sort()
nr.append(nr[-1]+3) # device joltage

socketJ = nr[0]
deviceJ = nr[-1]

diff1 = 0
diff2 = 0
diff3 = 0

for i, n in enumerate(nr):
    if (i == 0):
        continue
    ndiff = n - nr[i-1]
    if (ndiff > 3):
        print(f"WARNING: Joltage difference larger than 3 between {n} and {nr[i-1]}, adapter missing!")
    if (ndiff == 3):
        diff3 += 1
    elif (ndiff == 2):
        diff2 += 1
    elif (ndiff == 1):
        diff1 += 1
    
print(f"Task 1: There were {diff1} differences of one jolt, {diff2} differences of two jolts, and {diff3} differences of three jolts. Product of them is {diff1*diff3}")

def tribonacci(n):
    if (n < 3):
        print("ERROR: trionacci requires n >= 3!")
        return -1
    else:
        l = [0,1,1]
        for i in range(3,n):
            l.append(l[i-1] + l[i-2] + l[i-3])
        return l[-1]
    
redIdx = []     # redundant indices
redNrs = []     # redundant numbers
consecIdx = []  # consecutive indices
consecNrs =  [] # consecutive numbers
cdiff2 = 0   # count nrs with difference (right to left neighbour) of 2 and 3 (there can't be 1 or 0 as the values are distinct)
cdiff3 = 0

for i, n in enumerate(nr):
    if (i == 0) or (i == len(nr)-1):
        continue
    n2diff = nr[i+1] - nr[i-1]
    if (n2diff <= 3):
        redIdx.append(i)
        redNrs.append(n)
        if ((i-1) in redIdx):
            if (len(consecIdx) > 0) and ((i-1) in consecIdx[-1]):
                consecIdx[-1].append(i)
                consecNrs[-1].append(n)
            else:
                consecIdx.append([i-1,i])
                consecNrs.append([nr[i-1], n])
            #print(n2diff)
            if (n2diff == 3):
                cdiff3 += 1
            elif (n2diff == 2):
                cdiff2 += 1
        
redCount = len(redIdx) # Number of redundant numbers; without the restriction of 1..3 joltage difference,
                       # there would be 2**redCount possibilities to remove them
nbrCombs = 1           # count of combinations for the numbers within a sequence of redundant numbers
nbrConsecNrs = 0       # count of numbers in a sequence of consecutive numbers
for i in range(len(consecNrs)): # go through the sequences
    print(i, consecNrs[i], tribonacci(3+len(consecNrs[i])))
    nbrCombs *= tribonacci(3+len(consecNrs[i]))  # tribonacci(...) is the number of combinations from this sequence
    nbrConsecNrs += len(consecNrs[i])            

#nbrIndepNrs = len(nr)-2 - nbrConsecNrs  

totalNr = 2**(redCount-nbrConsecNrs)*nbrCombs  # 2**(...) is the number of combinations of standalone redundant numbers, 
                                               # and nbrCombs the number of combinations of numbers within sequences
    
print(f"Task 2: Total number of combinations is {totalNr}")


