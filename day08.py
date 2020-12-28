#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 05:58:49 2020

@author: marc
"""

lines = []
with open("input-day08", 'r') as f:
    lines = f.readlines()

cmds = []
val = []

for l in lines:
    cmds.append(l.split(' ')[0])
    val.append(l.split(' ')[1][:-1])

def execProg(cmds, val):
    cmdnrExec = []
    pc = 0
    acc = 0
    normalTermination = False
    while True:
        if (pc in cmdnrExec):
            #print("Detected infinite loop: Command nr", pc, "is executed the second time!")
            break
        else:
            cmdnrExec.append(pc)
        
        if (cmds[pc] == 'acc'):
            acc += int(val[pc])
        elif (cmds[pc] == 'jmp'):
            pc += int(val[pc]) - 1 # -1 because we increment below
        elif (cmds[pc] == 'nop'):
            pass
        else:
            print("Invalid command:", pc, cmds[pc])
        
        pc += 1
        
        if (pc == len(cmds)):
            print("Last command reached! Program done!")
            normalTermination = True
            break
    return acc, pc, normalTermination

acc, pc, normal = execProg(cmds, val)
print("Task 1: Final acc value:", acc, "at PC =", pc, "normal termination:", normal)

lineChanged = -1
for i, c in enumerate(cmds):
    if (c == 'acc'):
        continue
    else:
        if (c == 'jmp'):
            cmds_mod = cmds[:]
            cmds_mod[i] = 'nop'
        elif (c == 'nop'):
            cmds_mod = cmds[:]
            cmds_mod[i] = 'jmp'
        else:
            print("This shouldn't happen!")
        
        acc, pc, normal = execProg(cmds_mod, val)
        if normal:
            print("Normal Termination achieved!")
            lineChanged = i
            break

if normal:
    if (lineChanged >= 0):
        print("Task 2: Achieved normal termination by changing line", lineChanged, "which yields acc =", acc)
    else:
        print("Task 2: Nothing changed, normal termination")
else:
    print("Task 2: Tried all allowed replacements, but still no normal termination!")

    
