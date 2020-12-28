#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 21:46:11 2020

@author: marc
"""

import numpy as np

lines = []
with open("input-day5", 'r') as f:
    while(True):
        l = f.readline()[:-1]
        if (l == ''):
            break
        lines.append(l)


rowlist = []
seatlist = []

for l in lines:
    rows = np.array(range(128))
    for col in l[:7]:
        if (col == 'F'):
            rows = rows[:len(rows)//2]
        elif (col == 'B'):
            rows = rows[len(rows)//2:]
        else:
            print("Ill-formated row number!")
    rowlist.append(rows[0])
    
    seats = np.array(range(8))
    for col in l[7:]:
        if (col == 'L'):
            seats = seats[:len(seats)//2]
        elif (col == 'R'):
            seats = seats[len(seats)//2:]
        else:
            print("Ill-formated seat number!")
    seatlist.append(seats[0])

seatID = np.sort(np.array(rowlist) * 8 + np.array(seatlist))

freeSeats = []
for i in range(np.min(seatID), np.max(seatID)):
    if not (i in seatID):
        freeSeats.append(i)

print("Task 1: The maximum seat ID is", np.max(seatID))

if (len(freeSeats) > 1):
    print("Caution, multiple free seats! Cannot decide task 2!")
else:
    print("Task 2: My seat is nr", freeSeats[0])