#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 06:10:34 2020

@author: marc
"""

#import numpy as np

target = "shiny gold"

lines = []
with open("input-day7", 'r') as f:
    lines = f.readlines()

rules =[]
containslist = []
containstarget = []

for l in lines: 
    l = l[:-1]
    s = l.split(' contain ')
    defcat = s[0].split('bags')[0].rstrip()
    contcat = s[1].replace(' bags', '').replace(' bag', '')[:-1].split(', ')
    thisrule = []
    for c in contcat:
        nr, descr = c.split(' ', maxsplit=1)
        if (nr == 'no'):
            nr = 0
        else:
            nr = int(nr)
        if (descr != 'other'):
            thisrule.append((nr, descr))
        if (descr == target):
            containstarget.append(defcat)
    rules.append((defcat, thisrule))
    
containslist.append(list(set(containstarget))) # these are the level 1 containments (i.e. target is directly in there)
        
rules = dict(rules)

i = 0
while (len(containslist[i]) > 0): # for each recursion level...
    containscurlevel = []
    for key in rules.keys():      # ...walk through all rules...
        contlist = []
        for c in rules[key]:      # (O(1), could be done outside loop)
            contlist.append(c[1])
        for c in containslist[i]: # ...and within each rule, check for each item in containslist whether it is inculuded in this rule...
            if (c in contlist):
                duplicate = False #    ... and whether it's already in containslist
                if (key == target):
                    duplicate = True
                for j in range(i+1):
                    if key in containslist[j]:
                        duplicate = True
                if not duplicate: # if it's contained in the rule and not yet contained in containslist, then add it
                    containscurlevel.append(key)
    containslist.append(list(set(containscurlevel)))
    i += 1

containslist.remove([]) # remove empty last entry
# containslist[0]: all types which contain target
# containslist[n]: all types which contain types from containslist[n-1]

# Task 1: Total numbers of possibilities for wrapping target:
totalnr = 0
for l in containslist:
    totalnr += len(l)

# Task 2: Number of bags required
def calcContainedBags(target): 
    # calculated the nr of contained bags, including the target bag itself!
    if not rules[target]: # bag contains no other bags, stop recursion
        return 1   
    else:
        cursum = 0
        curlvl = rules[target]
        #print(curlvl)
        for c in curlvl:
            cursum += c[0] * calcContainedBags(c[1]) 
        cursum += 1 # add myself
        #print("  ", cursum)
        return cursum 
            

print("Task 1: found", len(containslist), "recursion levels for bag", target)
for i, l in enumerate(containslist):
    print("  ", len(l), "on level", i)
print("  In total:", totalnr, "possibilities to wrap target.")
print()
print("Task 2: Using", target, "bag requires", calcContainedBags(target)-1, "other bags.")



