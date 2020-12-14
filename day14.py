#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 05:59:57 2020

@author: marc
"""

#import numpy as np 
import itertools

with open("input-day14", 'r') as f:
    lines = list(f.read().splitlines())
    
addr = [] # contains address to be modified or -1 for "change mask"
vals = [] # contains values to be written to each adress
mask = [] #np.zeros(36, dtype=int)
maskadd = [] # np.zeros(36, dtype=int)
maskX = []

for l in lines:
    s = l.split(' = ')
    if s[0].startswith('mem'):
        addr.append(int(s[0].lstrip('mem[').rstrip(']')))
        vals.append(int(s[1]))
    elif s[0].startswith('mask'):
        addr.append(-1)
        vals.append(0)
        c = s[1]
        m = 0
        ma = 0
        mx = 0
        for i in range(len(s[1])):
            if (c[::-1][i] == '1'):
                m  += 2**i
                ma += 2**i
            elif (c[::-1][i] == 'X'):
                m  += 2**i
                mx += 2**i
        mask.append(m)
        maskadd.append(ma)
        maskX.append(mx)
    else:
        print("WARNING: Invalid command found:", l)

mp = -1 # mask pointer
memaddr = []
memvals = []
for i in range(len(addr)):
    if (addr[i] == -1):
        mp += 1
    else:
        if (addr[i] in memaddr):
            memvals.remove(memvals[memaddr.index(addr[i])])
            memaddr.remove(addr[i])
        memaddr.append(addr[i])
        memvals.append((vals[i] & mask[mp]) | maskadd[mp])

result = sum(memvals)

print(f"Task 1: Sum of all memory entries is {result}")

print("Solving Task 2...")
mp = -1 # mask pointer
memaddr = []
memvals = []
counter = 0

for i in range(len(addr)):
    if (i % 50 == 0):
        print("... processing cmd", i)
    if (addr[i] == -1):
        mp += 1
    else:
        multaddr = []
        baseaddr = addr[i] | mask[mp] # the address for which all X are 1
        multaddr.append(baseaddr)
        xbits = []
        perm = []
        flipvals = []
        for j in range(len(bin(maskX[mp]))-2):
            #print(j, bin(maskX[mp])[-j-1])
            if (bin(maskX[mp])[-j-1] == '1'):
                xbits.append([0,1])
            else:
                xbits.append([0])
        for p in itertools.product(*xbits):
            perm.append(p)
        for p in perm:
            f = 0
            for k, b in enumerate(p):
                if (b == 1):
                    f += 2**k
            flipvals.append(f)
        for f in flipvals[1:]:
            multaddr.append(baseaddr - f)
        
        for a in multaddr:
            if (a in memaddr):
                memvals.remove(memvals[memaddr.index(a)])
                memaddr.remove(a)
            memaddr.append(a)
            memvals.append(vals[i])
            counter += 1
            
result2 = sum(memvals)

print(f"Task 2: Sum of all memory entries is {result2}. {counter} writes to memory.") 