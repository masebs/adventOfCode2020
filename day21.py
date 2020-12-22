#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:58:55 2020

@author: marc
"""

with open("input-day21", 'r') as f:
    lines = list(f.read().splitlines())

allergs = []
food = []
allergFoods = {}
foodlist = []

for l in lines:
    l = l.split(' ')
    word = l.pop()
    curallergs = []
    while (word != "(contains"):
        curallergs.append(word[:-1])
        allergs.append(word[:-1])
        word = l.pop()
    for a in curallergs:
        if a not in allergFoods.keys():
            allergFoods[a] = []
    foodlist.append([[a for a in curallergs], []])
    while (len(l) > 0):
        word = l.pop()
        food.append(word)
        for a in curallergs:
            allergFoods[a].append(word)
        foodlist[-1][1].append(word)

allergIntersects = {}
for a in allergFoods.keys(): 
    allergsets = []
    for fl in foodlist:
        if a in fl[0]:
            allergsets.append(set(fl[1]))
    intersect = allergsets[0].intersection(*[s for s in allergsets[1:]])
    allergIntersects[a] = intersect

knownallergs = set([])
for ai in allergIntersects.keys():
    knownallergs = knownallergs.union(allergIntersects[ai])

nonallergs = set(food).difference(knownallergs)
count = 0
for na in nonallergs:
    count += food.count(na)

print(f"Task 1: The {len(nonallergs)} non-allergs are {nonallergs}.\nThey occur {count} times in the food list.")

allergMap = {}
keys = list(allergIntersects.keys())
k = 0
while len(allergMap) < len(set(allergs)):
#for ai in allergIntersects.keys():
    ai = keys[k%len(keys)]
    if len(allergIntersects[ai]) == 1:
        allergMap[ai] = list(allergIntersects[ai])[0]
        for i in keys:
            allergIntersects[i].discard(allergMap[ai])
    k += 1

keys = list(allergMap.keys())
keys.sort()
result = ""

for i in keys:
    result += allergMap[i] + ','
    
print(f"Task 2: The dangerous ingredient list is {result[:-1]}")
