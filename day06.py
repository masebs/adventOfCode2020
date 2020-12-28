#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 06:45:34 2020

@author: marc
"""

import numpy as np

lines = []
with open("input-day06", 'r') as f:
    while(True):
        l = f.readline()
        if (l == ''):
            break
        lines.append(l[:-1])
if (lines[-1] != ''):
    lines.append('')

groupanswers = []
groupresults_any = []
groupresults_all = []

for l in lines[:2089]:
    
    if (l == ''):
        # Obtain unique set of answers of this group
        astring = ''
        for a in groupanswers:
            astring += a
        s = set(astring)
        
        # Task 1: Result is number of different answers in this group
        groupresults_any.append(len(s))
        
        # Task 2: Need to check if answers are given by all group members
        # Very pythonesk, but actually slower than the other one:
        allAnswersCount = [[a in ga for ga in groupanswers] for a in s].count([True for x in range(len(groupanswers))])
        # Not so pythonesk, but apparently faster:
        allAnswersCount2 = 0
        for a in s:
            if all([a in ga for ga in groupanswers]):
                allAnswersCount2 += 1
        groupresults_all.append(allAnswersCount)        
        
        groupanswers = []
        
    else:
        groupanswers.append(l)

print("Task 1: Sum of positively answered questions by any group member over all groups is", np.array(groupresults_any).sum())
print("Task 2: Sum of positively answered questions by all group members over all groups is", np.array(groupresults_all).sum())
