#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 06:00:16 2020

@author: marc
"""

import numpy as np

with open("input-day20", 'r') as f:
    lines = list(f.read().splitlines())

i = 0
arrs = []
vals = []
nrs = []
while (i < len(lines)):
    l = lines[i]
    if (l == ''):
        arrs.append(np.array(vals))
    elif l.startswith('Tile'):
        nrs.append(int(l.lstrip('Tile ').rstrip(':')))
        vals = []
    else:
        vals.append([(1 if le == '#' else 0) for le in l])
    i += 1

arrs = np.array(arrs)
hasharr = np.zeros((arrs.shape[0], 4), dtype=int)
edgearr = np.zeros((arrs.shape[0], 4, arrs.shape[1]), dtype=int)
maparr  = np.zeros((arrs.shape[0], 4, 3), dtype=int) # will contain number of matching array and edge in last column

for i, a in enumerate(arrs):
    hasharr[i,0] = np.sum(a[0,:])
    edgearr[i,0,:] = arrs[i,0,:]
    hasharr[i,1] = np.sum(a[:,-1])
    edgearr[i,1,:] = arrs[i,:,-1]
    hasharr[i,2] = np.sum(a[-1,:])
    edgearr[i,2,:] = arrs[i,-1,:]
    hasharr[i,3] = np.sum(a[:,0])
    edgearr[i,3,:] = arrs[i,:,0]

hashmin, hashmax = np.amin(hasharr), np.amax(hasharr)

mapCount = 0
for i in range(hashmin, hashmax+1):
    #print(f"hash={i}")
    compArrs, compEdge = np.where(hasharr == i)
    for j in range(compArrs.shape[0]):
        for k in range(compArrs.shape[0]):
            if (compArrs[j] != compArrs[k]):
                #print(f"  i={i},j={j},k={k}, checking tiles {nrs[compArrs[j]]} and {nrs[compArrs[k]]}")
                if all(edgearr[compArrs[j], compEdge[j], :] == edgearr[compArrs[k], compEdge[k], :]):
                    #print('  match!')
                    maparr[compArrs[j], compEdge[j]] = (compArrs[k], compEdge[k], 0) # last comp: don't flip
                    #maparr[compArrs[k], compEdge[k]] = (compArrs[j], compEdge[j], 0)
                    mapCount += 1
                elif all(edgearr[compArrs[j], compEdge[j], ::-1] == edgearr[compArrs[k], compEdge[k], :]):
                    #print('  match!')
                    maparr[compArrs[j], compEdge[j]] = (compArrs[k], compEdge[k], 1) # last comp: flip!
                    #maparr[compArrs[k], compEdge[k]] = (compArrs[j], compEdge[j], 1)
                    mapCount += 1

print(f"Mapped {mapCount} out of {4*arrs.shape[0]-int(4*np.sqrt(arrs.shape[0]))} non-corner edges")         

# count 0 lines in maparr, those with two non-zero lines  are corners!
cornerIDs = []
cornerIdx = []
edgeIdx = []
mapped = []
unmappedArrs = []
for k, m in enumerate(maparr):
    unmapped = 0
    for i in range(maparr.shape[1]):
        if all(m[i,:] == [0,0,0]):
            unmapped += 1
    if (unmapped == 2):
        cornerIDs.append(nrs[k])
        cornerIdx.append(k)
    elif (unmapped == 1):
        edgeIdx.append(k)
    elif (unmapped == 0):
        mapped.append(k)
    else:
        unmappedArrs.append(k)

product = 1
for i in range(len(cornerIDs)):
    product *= cornerIDs[i]

print(f"\nTask 1: Product of the corners' ids is {product}")

def flipArr(arr, myedge, appedge, flip, reduce=True):
    if ([myedge, appedge] in [[0,1], [1,2], [2,3], [3,0]]): # rotate clockwise
        if reduce: 
            newarr = np.zeros((arr.shape[0]-2, arr.shape[1]-2), dtype=int)
        else:
            newarr = np.zeros((arr.shape[0], arr.shape[1]), dtype=int)
        for i in range(newarr.shape[0]):
            if reduce:
                newarr[i,:] = arr[1:-1, i+1]
            else:
                newarr[i,:] = arr[:, i]
        #if ([myedge, appedge] in [[0,1], [1,2], [2,3], [3,0]]):
        newarr = newarr[:, -1::-1] # additional flip in the other axis required for those
        if ([myedge, appedge] in [[0,1], [2,3]]):
            if flip:
                return newarr[:, -1::-1]
            else:
                return newarr[:,:]
        else:
            if flip:
                return newarr[-1::-1,:]
            else:
                return newarr[:,:]
        
    elif ([myedge, appedge] in [[1,0], [2,1], [3,2], [0,3]]): # rotate counter-clockwise
        if reduce:
            newarr = np.zeros((arr.shape[0]-2, arr.shape[1]-2), dtype=int)
        else:
            newarr = np.zeros((arr.shape[0], arr.shape[1]), dtype=int)
        for i in range(newarr.shape[1]):
            if reduce:
                newarr[:,i] = arr[i+1, 1:-1]
            else:
                newarr[:,i] = arr[i, :]
#        if ([myedge, appedge] in [[2,1], [0,3]]):
        newarr = newarr[-1::-1, :] # additional flip in the other axis required for those
        if ([myedge, appedge] in [[1,0], [3,2]]):
            if flip:
                return newarr[:, :]
            else:
                return newarr[-1::-1,:] # and invert flip here!
        else:
            if flip:
                return newarr[:, -1::-1]
            else:
                return newarr[:,:]
        
    elif ([myedge, appedge] in [[0,2], [2,0]]): # appending north to south
        if flip:
            if reduce: 
                return arr[1:-1, -2:0:-1] # flip columns
            else:
                return arr[:, -1::-1] # flip columns
        else:
            if reduce:
                return arr[1:-1, 1:-1]
            else:
                return arr[:,:]
    elif ([myedge, appedge] in [[1,3], [3,1]]): # appending east to west
        if flip:
            if reduce:
                return arr[-2:0:-1, 1:-1] # flip lines
            else:
                return arr[-1::-1,:]
        else:
            if reduce:
                return arr[1:-1, 1:-1]
            else:
                return arr[:,:]
    elif ([myedge, appedge] in [[0,0], [2,2]]):
        if flip:
            if reduce:
                return arr[-2:0:-1, -2:0:-1] # flip lines and columns
            else:
                return arr[-1::-1, -1::-1]
        else:
            if reduce:
                return arr[-2:0:-1, 1:-1]    # flip lines only
            else:
                return arr[-1::-1, :]
    elif ([myedge, appedge] in [[1,1], [3,3]]):
        if flip:
            if reduce:
                return arr[-2:0:-1, -2:0:-1] # flip lines and columns
            else:
                return arr[-1::-1, -1::-1]
        else:
            if reduce:
                return arr[1:-1, -2:0:-1]    # flip columns only
            else:
                return arr[:, -1::-1]
    else:
        print("Shouldn't happen!")
        
    
## Assemble the map
# look for top left corner
topleftid = -99
for c in cornerIdx:
    if all(maparr[c,0] == [0,0,0]) and all(maparr[c,3] == [0,0,0]):
        topleftid = c
        break
    
def getEdge(arr, edge):
    if edge == 0:
        return arr[0,:]
    elif edge == 1:
        return arr[:,-1]
    elif edge == 2:
        return arr[-1,:]
    elif edge == 3:
        return arr[:,0]
    
def getAllEdges(arr):
    return np.array([arr[0,:], arr[:,-1], arr[-1,:], arr[:,0]])

# find array map line by line
curidx = topleftid
leftidx = topleftid
arrayidcs = []
leftarrs = [np.array([topleftid, 2, 0])]
arraylines = []
dims = int(np.sqrt(arrs.shape[0]))

arrdims = arrs.shape[1]-2 #len(arraylines[0])+1
assarr = np.zeros((arrdims*dims, arrdims*dims), dtype=int) # the assembled array
fdims = arrdims+2
fullarr = np.zeros((fdims*dims, fdims*dims), dtype=int)
usedArrs = []

for i in range(dims): 
    line = [] 
    arrayidcs.append(curidx)

    if (i == 0):
        assarr[i*arrdims:(i+1)*arrdims, :arrdims] = flipArr(arrs[curidx], 2, 0, 0)
        fullarr[i*fdims:(i+1)*fdims, :fdims] = flipArr(arrs[curidx], 2, 0, 0, reduce=False)
        oldleftarray = flipArr(arrs[curidx], 2, 0, 0, reduce=False)
        usedArrs.append(curidx)
        oldharray = oldleftarray
        oldhidx = curidx
        oldvidx = curidx
    else:
        curidx = 999
        fromedge = getEdge(oldleftarray, 2)
        for anr, a in enumerate(arrs):
            a = arrs[anr]
            if anr in usedArrs:
                continue
            edges = getAllEdges(a)
            for enr, e in enumerate(edges):
                if all(e == fromedge):
                    oldvidx = curidx
                    curidx = anr
                    toedge = enr
                    flip = 0
                    usedArrs.append(curidx)
                    break
                elif all(e[::-1] == fromedge):
                    oldvidx = curidx
                    curidx = anr
                    toedge = enr
                    flip = 1
                    usedArrs.append(curidx)
                    break
            if curidx != 999:
                break
        
        if toedge == 3:
            flip = 0
        print(f"Vert: Appending arr {curidx}, toedge {toedge}, flip {flip}")
        assarr[i*arrdims:(i+1)*arrdims, :arrdims] = flipArr(arrs[curidx], 2, toedge, flip)
        fullarr[i*fdims:(i+1)*fdims, :fdims] = flipArr(arrs[curidx], 2, toedge, flip, reduce=False)
        oldleftarray = flipArr(arrs[curidx], 2, toedge, flip, reduce=False)
        oldharray = oldleftarray
        oldhidx = curidx
        
    for j in range(1,dims): # go through one line     
        curidx = 999
        fromedge = getEdge(oldharray, 1)
        for anr, a in enumerate(arrs):
            a = arrs[anr]
            if anr in usedArrs:
                continue
            edges = getAllEdges(a)
            for enr, e in enumerate(edges):
                if all(e == fromedge):
                    oldhidx = curidx
                    curidx = anr
                    toedge = enr
                    flip = 0
                    usedArrs.append(curidx)
                    break
                elif all(e[::-1] == fromedge):
                    oldhidx = curidx
                    curidx = anr
                    toedge = enr
                    flip = 1
                    usedArrs.append(curidx)
                    break
            if curidx != 999:
                break
            
        print(f" Hor: Appending arr {curidx}, toedge {toedge}, flip {flip}")
        assarr[i*arrdims:(i+1)*arrdims, j*arrdims:(j+1)*arrdims] = flipArr(arrs[curidx], 1, toedge, flip)
        fullarr[i*fdims:(i+1)*fdims, j*fdims:(j+1)*fdims] = flipArr(arrs[curidx], 1, toedge, flip, reduce=False)
        oldharray = flipArr(arrs[curidx], 1, toedge, flip, reduce=False)
        while not all(fullarr[i*fdims:(i+1)*fdims,j*fdims-1] == fullarr[i*fdims:(i+1)*fdims,j*fdims]):
            print("WARNING: Full array mismatch at i=", i, ", j=",j)
            flip = int(not(flip))
            print(f"   Retry: Hor: Appending arr {curidx}, toedge {toedge}, flip {flip}")
            assarr[i*arrdims:(i+1)*arrdims, j*arrdims:(j+1)*arrdims] = flipArr(arrs[curidx], 1, toedge, flip)
            fullarr[i*fdims:(i+1)*fdims, j*fdims:(j+1)*fdims] = flipArr(arrs[curidx], 1, toedge, flip, reduce=False)
            oldharray = flipArr(arrs[curidx], 1, toedge, flip, reduce=False)
        
        line.append([curidx, toedge, flip])
        arrayidcs.append(curidx)
        
    arraylines.append(line)
        

# load monster pattern
with open("input-day20-pattern", 'r') as f:
    lines = list(f.read().splitlines())
pattern = []
for i,l in enumerate(lines):
    for j,c in enumerate(l):
        if (c == "#"):
            pattern.append([j,i])
pxmax = max([p[0] for p in pattern])
pymax = max([p[1] for p in pattern])

psums = []
monster_coords = [(0, 1), (1, 2), (4, 2), (5, 1), (6, 1), (7, 2), (10, 2), (11, 1), (12, 1), (13, 2), (16, 2), (17, 1), (18, 0), (18, 1), (19, 1)]
monster_w = max(x for x, y in monster_coords) + 1
monster_h = max(y for x, y in monster_coords) + 1
monstercoords = []

def monsterCount(pattern, assarr):
    l = 0
    c = 0
    monstercount = 0
    waterInMonsterCount = 0
    
    
    for l in range(assarr.shape[0] - pxmax):
        for c in range(assarr.shape[1] - pymax):
            wc = 0
            psum = 0
            for p in pattern:
                psum += assarr[l+p[0], c+p[1]]
            psums.append(psum)
            if (psum == len(pattern)):
                monstercoords.append([l,c])
                print(l, c)
                monstercount += 1
                waterInMonsterCount += wc
    return monstercount

count = np.zeros(2, dtype=int)

count += monsterCount(pattern, assarr)
count += monsterCount(pattern, assarr[::-1,:])
count += monsterCount(pattern, assarr[:,::-1])
#count += monsterCount(pattern, assarr[::-1,::-1])

newarr = np.zeros((assarr.shape[0], assarr.shape[1]), dtype=int)
for i in range(newarr.shape[0]):
    newarr[i,:] = assarr[:, i]
newarr = newarr[:,::-1]
count += monsterCount(pattern, newarr)
count += monsterCount(pattern, newarr[::-1,:])
count += monsterCount(pattern, newarr[:,::-1])
#count += monsterCount(pattern, newarr[::-1,::-1]) # the same as newarr3

newarr2 = np.zeros((newarr.shape[0], newarr.shape[1]), dtype=int)
for i in range(newarr2.shape[0]):
    newarr2[i,:] = newarr[:, i]
newarr2 = newarr2[:,::-1]
count += monsterCount(pattern, newarr2)
#count += monsterCount(pattern, newarr2[::-1,:])
#count += monsterCount(pattern, newarr2[:,::-1])
#count += monsterCount(pattern, newarr2[::-1,::-1])
#
newarr3 = np.zeros((newarr.shape[0], newarr.shape[1]), dtype=int)
for i in range(newarr3.shape[0]):
    newarr3[i,:] = newarr2[:, i]
newarr3 = newarr3[:,::-1]
count += monsterCount(pattern, newarr3)
#count += monsterCount(pattern, newarr3[::-1,:])
#count += monsterCount(pattern, newarr3[:,::-1]) # the same as newarr[::-1,:]
#count += monsterCount(pattern, newarr3[::-1,::-1])

mc = count[0]
wmc = count[1]

waterCount = len(np.where(assarr == 1)[0])
waterInMonsterCount = len(pattern) #len(np.where(pattern == 1)[0])
habitatWaterCount = waterCount - mc*waterInMonsterCount

print(f"Task 2: {mc} monsters found. Water count in habitat: {habitatWaterCount}")

t = np.array([[0,0,0,0,0], [0,1,2,3,0], [0,4,5,6,0], [0,7,8,9,0], [0,0,0,0,0]])
#t = np.array([[0,0,0,0,0,0], [0,1,2,3,4,0], [0,5,6,7,8,0], [0,9,10,11,12,0], [0,13,14,15,16,0], [0,0,0,0,0,0]])

def printArr(arr):
    for l in arr:
        for c in l:
            if c == 1:
                print('#', sep='', end='')
            else:
                print('.', sep='', end='')
        print('\n', sep='', end='')