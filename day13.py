#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 06:10:46 2020

@author: marc
"""

import numpy as np 

with open("input-day13", 'r') as f:
    lines = list(f.read().splitlines())

timestamp = int(lines[0])
lines[1] = lines[1].split(',')

nrs = [] # bus lines to be investigated, 0 for x (don't care)
for c in lines[1]:
    if (c == 'x'):
        nrs.append(0)
    else:
        nrs.append(int(c))

### Task 1: Find next time (from earliest possible time) where time % busline = 0
nextbus = 0
departsAt = 0
for i in range(timestamp, timestamp+max(nrs)):
    for l in nrs:
        if (l == 0):
            continue
        if (i % l == 0):
           nextbus = l
           departsAt = i
    if (nextbus > 0):
        break

waitTime = departsAt - timestamp

print(f"Task 1: next possible bus is {nextbus}, departs at {departsAt}, waiting time {waitTime}, product {nextbus * waitTime}")

### Task 2
nrs = np.array(nrs)                             # switch to numpy
maxnr, maxidx = np.amax(nrs), np.argmax(nrs)    # max value and its index
otherlist = np.where(nrs > 0)[0]                # non-zero bus lines (those we care about)
idiff = np.zeros(otherlist.shape[0], dtype=int) # this will be the time offsets of the bus lines to the first (maximum) bus line
vals = np.zeros(otherlist.shape[0], dtype=int)  # this will be the numbers of the bus lines we care about 

for j, k in enumerate(otherlist):
    idiff[j] = k - maxidx
    vals[j] = nrs[k]
    
# sort vals and idiff in ascending order (w.r.t. vals); not really necessary, but this might provide the fastest progress
#   (funnily, it actually takes a few less iterations if we sort it descending)
sortidcs = np.argsort(vals)
vals = vals[sortidcs][::-1]
idiff = idiff[sortidcs][::-1]

# initialize stuff for the loop below
found = False       # loop condition
tfound = -1         # the result
i = 0               # loop counter         
inc = vals[0]       # initial increment for loop counter
countLoops = 0      # counts the number of actual loops
valsCovered = 0     # counts the number of vals for which a remainder 0 has already been found

# Loop: Increase time stamp by inc, and look for a remainder 0 for the next vals[j] where we haven't found one yet.
#       Then, multiply increment by vals[j], as there can be no relevant values before that increment
while not found:
    i += inc 
    countLoops += 1
    found = True
    
    for j in range(valsCovered+1, idiff.shape[0]):  # this loop will usually only be executed once, maximum twice (when remainder 0 found)
        if ((i+idiff[j]) % vals[j] == 0):           # if the remainder is 0 for vals[j], we can multiply inc by it, and we are done with vals[j]
            print(f" Found {i+idiff[j]} mod {vals[j]} == 0")
            inc *= vals[j]                          # use increased increment from here on
            valsCovered += 1                        # don't check vals[j] any more in the future
            print(f"   multiplying inc by {vals[j]}, now inc = {inc}")
        else:                                       # no remainder 0 found for vals[j]
            found = False                           # so i is not the number we are looking for
            break                                   # continue with next iteration of outer loop
        
    if found:                # remainder was 0 for all values in vals, so we've got it!
        tfound = i - maxidx  # calculate timestamp which belongs to the first element in the unsorted vals array

print(f"Task 2: First timestamp fulfilling requirements is {tfound}. Found it in {countLoops} loop iterations.")
