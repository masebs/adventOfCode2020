#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 06:44:32 2020

@author: marc
"""
#from random import random

ID = 0

class Tile:
    def __init__(self):
        global ID
        self.n = dict()
        for i in range(6):
            self.n[i] = None # 0 = ne, 1 = e, 2 = se, 3 = sw, 4 = w, 5 = nw
        self.flipped = False
        self.ID = ID
#        self.dist = 0
#        self.done = False
        ID += 1
    
    def getNeighbors(self):
        return [self.n[i] for i in self.n.keys()]

def buildMesh(size):
    if size % 2 != 0: #  build an even number of rows and cols to make it easier
        size += 1
    tl = [[Tile() for y in range(size)] for x in range(size)]
    for y in range(size):
        for x in range(size):
            t = tl[y][x]
            if y == 0:
                if x == 0:
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x]
                elif x == size-1:
                    t.n[2] = tl[y+1][x]
                    t.n[3] = tl[y+1][x-1]
                    t.n[4] = tl[y][x-1]
                else:
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x]
                    t.n[3] = tl[y+1][x-1]
                    t.n[4] = tl[y][x-1]
            elif y == size-1:
                if x == 0:
                    t.n[0] = tl[y-1][x+1]
                    t.n[1] = tl[y][x+1]
                    t.n[5] = tl[y-1][x]
                elif x == size-1:
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x]
                else:
                    t.n[0] = tl[y-1][x+1]
                    t.n[1] = tl[y][x+1]
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x]
            elif y % 2 == 1:
                if x == 0:
                    t.n[0] = tl[y-1][x+1]
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x+1]
                    t.n[3] = tl[y+1][x]
                    t.n[5] = tl[y-1][x]
                elif x == size-1:
                    t.n[3] = tl[y+1][x]
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x]
                else:
                    t.n[0] = tl[y-1][x+1]
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x+1]
                    t.n[3] = tl[y+1][x]
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x]
            else: # y % 2 == 0
                if x == 0:
                    t.n[0] = tl[y-1][x]
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x]
                elif x == size-1:
                    t.n[0] = tl[y-1][x]
                    t.n[2] = tl[y+1][x]
                    t.n[3] = tl[y+1][x-1]
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x-1]
                else:
                    t.n[0] = tl[y-1][x]
                    t.n[1] = tl[y][x+1]
                    t.n[2] = tl[y+1][x]
                    t.n[3] = tl[y+1][x-1]
                    t.n[4] = tl[y][x-1]
                    t.n[5] = tl[y-1][x-1]
    return tl
# First try with a BFS-style buildup from the center cell 
# Seems elegant at the first glance, but is horribly slow, as the corresponding graph has many many edges and BFS is O(|V|+|E||)
#def buildMesh(tile, maxrec, reclvl=0, tileList=[])
#    dlist = list(range(6))
#    ndir = len(dlist)
#    q = [tile]
#    
#    while len(q) > 0:
##        print(len(q))
#        t = q.pop(0)
#        t.done = True
#        for d in dlist:
#            if t.n[d] == None:
#                t.n[d] = Tile()
#                t.n[d].dist = t.dist + 1
#                tileList.append(t.n[d])
#                t.n[d].n[(d+3)%ndir] = t # set myself as neighbor
#                if t.n[(d+1)%ndir] != None: # there is already a clockwise neighbor
#                    t.n[d].n[(d+2)%ndir] = t.n[(d+1)%ndir]
#                    t.n[(d+1)%ndir].n[(d-1)%ndir] = t.n[d]
#                if t.n[(d-1)%ndir] != None: # there is already an anti-clockwise neighbor
#                    t.n[d].n[(d-2)%ndir] = t.n[(d-1)%ndir]
#                    t.n[(d-1)%ndir].n[(d+1)%ndir] = t.n[d]
#
#        neighbors = t.getNeighbors()
#        if t.dist < maxrec:
#            for n in neighbors:
#                if n != None and not all(n.n) and not n.done:
#                    q.append(n)      
#        done.append(t)

    return tileList

def go(tile, d):
    if d == 'ne':
        return tile.n[0]
    elif d == 'e':
        return tile.n[1]
    elif d == 'se':
        return tile.n[2]
    elif d == 'sw':
        return tile.n[3]
    elif d == 'w':
        return tile.n[4]
    elif d == 'nw':
        return tile.n[5]
    else:
        print("Invalid direction!")
        return None
    
with open("input-day24", 'r') as f:
    lines = list(f.read().splitlines())

tiles = []
for l in lines:
    dirs = []
    newdir = ''
    for d in l:
        if d in ['n', 's']:
            newdir = d
        elif d in ['e', 'w']:
            if newdir in ['n','s']:
                newdir += d
                dirs.append(newdir)
                newdir = ''
            else:
                dirs.append(d)
                newdir = ''
    tiles.append(dirs)

print("Building mesh...")
size = 160
tileList = buildMesh(size)
starttile = tileList[size//2][size//2]

print("Start flipping...")
for t in tiles:
    curt = starttile
    for d in t:
        curt = go(curt, d)
    curt.flipped = not(curt.flipped)

curt = starttile

flippedCount = 0
for row in tileList:
    for t in row:
        if t.flipped:
            flippedCount += 1
        
print(f"Task 1: {flippedCount} tiles are flipped.")

ndays = 100
fcounts = []
fcounts.append(flippedCount) # initial state
for n in range(ndays):
    fliplist = []
    for row in tileList: # check which tiles to flip
        for t in row:
            nflipcount = 0
            for k in t.n.keys():
                if t.n[k] != None and t.n[k].flipped:
                    nflipcount += 1
            if t.flipped and (nflipcount == 0 or nflipcount > 2):
                fliplist.append(t)
            elif not t.flipped and nflipcount == 2:
                fliplist.append(t)
    for t in fliplist: # flip them
        t.flipped = not(t.flipped)
    flippedCount = 0
    for row in tileList: # count flipped tiles
        for t in row:
            if t.flipped:
                flippedCount += 1
    fcounts.append(flippedCount)

print(f"Task 2: {fcounts[-1]} tiles are flipped after {ndays} days.") 