#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 05:58:07 2020

@author: marc
"""

import numpy as np 
from itertools import product

with open("input-day17", 'r') as f:
    lines = list(f.read().splitlines())

k = 2
l = 2
m = np.zeros([len(lines)+2, len(lines)+2, len(lines)+2, len(lines)+2], dtype=bool)
for i,lin in enumerate(lines):
    for j,c in enumerate(lin):
        if (c == '#'):
            m[i+1,j+1,k,l] = 1
#print(m[:,:,0]); print(m[:,:,1]); print(m[:,:,2])

def doCycle(m):
    imax = m.shape[0]-1
    jmax = m.shape[1]-1
    kmax = m.shape[2]-1
    lmax = m.shape[3]-1
    nm = np.copy(m)
    for i in range(imax+1):
        for j in range(jmax+1):
            for k in range(kmax+1):
                for l in range(lmax+1):
                    neighbours = list(product([max(0,i-1), i, min(imax,i+1)], [max(0,j-1), j, min(jmax,j+1)], [max(0,k-1), k, min(kmax,k+1)], [max(0,l-1), l, min(lmax,l+1)]))
                    neighbours = list(set(neighbours)) # remove duplicates (can occur at the boundaries)
                    neighbours.remove((i,j,k,l)) # remove current cube itself
                    
                    count = 0
                    activeNlist = []
                    for n in neighbours:
                        if m[n]:
                            count += 1
                            activeNlist.append(n)
                    if m[i,j,k,l] and not (count == 2 or count == 3):
                        nm[i,j,k,l] = 0
                    elif (not m[i,j,k,l]) and (count == 3):
                        nm[i,j,k,l] = 1
                    #print(i,j,k,count, m[i,j,k], nm[i,j,k])#activeNlist)
    return nm
                    
def extendMap(m):
    nm = np.zeros((m.shape[0]+2, m.shape[1]+2, m.shape[2]+2, m.shape[3]+2), dtype=bool)
    for i in range(1, nm.shape[0]-1):
        for j in range(1, nm.shape[1]-1):
            for k in range(1, nm.shape[2]-1):
                for l in range(1, nm.shape[3]-1):
                    nm[i,j,k,l] = m[i-1,j-1,k-1,l-1]
    return nm
 
for i in range(6):
    m = doCycle(m)
    m = extendMap(m)
    
print(f"Task 2: Sum of active elements: {np.sum(m)}")