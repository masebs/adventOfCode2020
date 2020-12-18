#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 05:59:49 2020

@author: marc
"""

def parseInfix(exp):
    #print("parseInfix, exp =", exp)
    i = 0
    leftop = None
    op = None
    exp = exp.replace(' ', '') # remove whitespace
    
    while (i < len(exp)):
        c = exp[i]
        
        if (c == '('):
            substart = i + 1
            subend = substart
            levelcounter = 0
            while (levelcounter >= 0): 
                if(exp[subend] == '('):
                    levelcounter += 1
                elif(exp[subend] == ')'):
                    levelcounter -= 1
                subend += 1
            subend -= 1
            subres = parseInfix(exp[substart:subend])
            if (leftop == None): # bracket is the begin of exp
                leftop = subres
            elif (op == '+'):
                leftop += subres
            elif (op == '*'):
                leftop *= subres
            i += subend - substart + 1 # jump over sub-expression including both brackets

        elif (c == ')'):
            print("WARNING: Closing bracket remained in expression! Shouldn't happen!")
            
        elif (c in ['+', '*']):
            op = c

        else: # Number
            if (leftop == None):
                leftop = int(c)
            else:
                rightop = int(c)
                if (op == '+'):
                    leftop += rightop
                elif (op == '*'):
                    leftop *= rightop
                else:
                    print("Shouldn't happen!")     
        i += 1
    return leftop
    
with open("input-day18", 'r') as f:
    lines = list(f.read().splitlines())

#l = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
#print(parseInfix(l))

result = 0

for l in lines:
    result += parseInfix(l)

print(f"Task 1: Sum is {result}")