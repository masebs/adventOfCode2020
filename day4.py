#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 20:18:00 2020

@author: marc
"""
#import numpy as np
import re

with open("input-day4", 'r') as f:
    lines = f.readlines()

pplist = []         # full passport data
pplistCatOnly = []  # only categories, no values
curVals = []
curCats = []

# Parse Passports from input and store them in pplist
for i, l in enumerate(lines):
    if (l == '\n'):
        pplist.append(curVals)
        pplistCatOnly.append(curCats)
        curVals = []
        curCats = []
        
    fields = l.split(' ')
    for f in fields:
        if (len(f) > 3 and len(f.split(':')) == 2):
            cat, val = f.split(':')
            if (val[-1] == '\n'):
                val = val[:-1]
            curVals.append([cat, val])
            curCats.append(cat)
            
if (curVals != pplist[-1]): # add the last one in case it is still missing (no newline at end of file)
    pplist.append(curVals)
    pplistCatOnly.append(curCats)

# Go through pplist and validate passports
requiredStrict = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'])
requiredLoose = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
#print(requiredStrict)
#print(requiredLoose)

strictlyValidCounter = 0        # just for info
looselyValidCounter = 0         # for task 1
reallyLooselyValidCounter = 0   # for task 2
totalCounter = 0

for i in range(len(pplist)):
    p = pplistCatOnly[i]
    pp = pplist[i]
    totalCounter += 1
    if (requiredStrict.issubset(set(p))):
        strictlyValidCounter += 1
    if (requiredLoose.issubset(set(p))):
        looselyValidCounter += 1
        ppdict = dict(pp)
        if (1920 <= int(ppdict["byr"]) <= 2002) and (2010 <= int(ppdict["iyr"]) <= 2020) and (2020 <= int(ppdict["eyr"]) <= 2030) \
        and ((ppdict["hgt"][-2:] == "cm" and 150 <= int(ppdict["hgt"][:-2]) <= 193) or (ppdict["hgt"][-2:] == "in" and 59 <= int(ppdict["hgt"][:-2]) <= 76)) \
        and ((ppdict["hcl"][0] == '#') and bool(re.match("[0-9,a-f][[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]$", ppdict["hcl"][1:]))) \
        and (ppdict["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]) \
        and bool(re.match("[0-9]{9}$", ppdict["pid"])):
            reallyLooselyValidCounter += 1
            
    
print("Task 1: Checked", totalCounter, "passports, of which", strictlyValidCounter, "were strictly and", looselyValidCounter, "loosely valid.")
print("Task 2:", reallyLooselyValidCounter, "are loosely valid in terms of field as well as data.")
    
    