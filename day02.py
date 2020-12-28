#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:00:39 2020

@author: marc
"""

import numpy as np

f = open("input-day02", 'r')

lines = f.readlines()

countValid = 0
countInvalid = 0
countValidT2 = 0
countInvalidT2 = 0

for l in lines:
    charnrs, char, pwd = l.split(' ')
    charnrFrom, charnrTo = np.array(charnrs.split('-'), dtype=int)
    char = char.replace(':', '')
    pwd = pwd[:-1]
    
    # Task 1
    if (charnrFrom <= pwd.count(char) <= charnrTo):
        countValid += 1
        #print('VALID:', charnrFrom, '-', charnrTo, char, pwd)
    else:
        countInvalid += 1
        #print('INVALID:', charnrFrom, '-', charnrTo, char, pwd)
        
    # Task 2
    if (pwd[charnrFrom-1] == char):
        if not(pwd[charnrTo-1] == char):
            countValidT2 += 1
        else:
            countInvalidT2 += 1
    else:
        if (pwd[charnrTo-1] == char):
            countValidT2 += 1
        else:
            countInvalidT2 += 1
            

print('Result Task 1:', countValid, 'out of', countValid+countInvalid, 'passwords are valid!')  
print('Result Task 2:', countValidT2, 'out of', countValidT2+countInvalidT2, 'passwords are valid!') 

f.close()    
