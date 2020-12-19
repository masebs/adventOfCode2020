#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 06:43:59 2020

@author: marc
"""

def traceRule(rules, rnr):
    #print("e",rnr)
    if (type(rules[rnr][0][0]) == str): # these are single letters, just return them (end of recursion)
        return rules[rnr][0][0]
    elif (len(rules[rnr]) == 1):        # these are elementary rules (without |), we can concatenate the single letters 
        newnrs = rules[rnr][0]
        res1 = []
        isAtomic = True
        for n in newnrs:
            app = traceRule(rules, n)
            if (type(app) == list):
                for le in app:
                    if (len(le) > 1) or (len(app) > 1):
                        isAtomic = False
            res1.append(traceRule(rules, n))
        if (len(newnrs) == 1): # for trivial rules: unpack
            res1 = res1[0]
        res1 = expand(res1)#flattenlist(res1)
        if isAtomic:
            res1 = [''.join(res1)]
        return res1 #''.join(flattenList(res1))
    else:       # these are rules with | -> we need the cartesian product of the rules on both sides of the |
        newnrs1 = rules[rnr][0]
        newnrs2 = rules[rnr][1]
        if (len(newnrs1) == 2 and len(newnrs2) == 2):
            l1 = expand(traceRule(rules, newnrs1[0]))
            l2 = expand(traceRule(rules, newnrs1[1]))
            if (all(isinstance(le, list) for le in [l1,l2])):
                res1 = [x+y for x in l1 for y in l2]
            elif (isinstance(l1, list)):
                res1 = [x+l2 for x in l1]
            elif (isinstance(l2, list)):
                res1 = [l1+y for y in l2]
            else:
                res1 = l1+l2
                
            l1 = expand(traceRule(rules, newnrs2[0]))
            l2 = expand(traceRule(rules, newnrs2[1]))
            if (all(isinstance(le, list) for le in [l1,l2])):
                res2 = [x+y for x in l1 for y in l2]
            elif (isinstance(l1, list)):
                res2 = [x+l2 for x in l1]
            elif (isinstance(l2, list)):
                res2 = [l1+y for y in l2]
            else:
                res2 = l1+l2
                
        else:
            res1 = traceRule(rules, newnrs1[0])
            res2 = traceRule(rules, newnrs2[0])
        res = flattenList([res1, res2]) #flattenList(flattenList([res1, res2]))
        return res

def flattenList(l):
    if (type(l) != list):
        return l
    else:
        ret = []
        for el in l:
            if (type(el) == list):
                ret += el
            else:
                ret.append(el)
        return ret

def expand(l):
    if (len(l) == 2):
        if (all(isinstance(le, list) for le in l)):
            return [x+y for x in l[0] for y in l[1]]
        elif (isinstance(l[0], list)):
            return [x+l[1] for x in l[0]]
        elif (isinstance(l[1], list)):
            return [l[0]+y for y in l[1]]
        else:
            return l
    elif (len(l) > 2):
        if any(isinstance(le, list) for le in l):
            print("WARNING!")
        return l
    else: 
        return l
        

with open("input-day19", 'r') as f:
    lines = list(f.read().splitlines())

rules = {}
for r in lines[:lines.index('')]:
    rname, rdef = r.split(': ')
    rules[int(rname)] = [rdef.split(' | ')[0].split(' '), 
          rdef.split(' | ')[1].split(' ') if len(rdef.split(' | ')) > 1 else None] 
for r in rules.keys():
    if (rules[r][0][0].isnumeric()):
        rules[r][0] = list(map(int, rules[r][0]))
    else:
        rules[r][0][0] = rules[r][0][0].rstrip('"').lstrip('"')
    if (rules[r][1] == None):
        rules[r].remove(None)
    if (len(rules[r]) > 1) and (rules[r][1][0].isnumeric()):
        rules[r][1] = list(map(int, rules[r][1]))

messgs = [m for m in lines[lines.index('')+1:]]

## build list of allowed strings
#tr0 = traceRule(rules, 0)
#tr1 = traceRule(rules, 1)
#tr2 = traceRule(rules, 2)
#tr3 = traceRule(rules, 3)
#tr4 = traceRule(rules, 4)

#for i in range(max(rules.keys()), 0, -1):
#    traceRule(rules, i)

r0 = traceRule(rules, 0)
r8 = traceRule(rules,8)
r11 = traceRule(rules,11)

pattern = r0
sepPattern = [r8, r11]

patternLengths = list(set(map(len, pattern)))


validCount = 0
lengths = []
for m in messgs:
    lengths.append(len(m))
    #validTotal = False
    c = 0
    valid = False
    
    # faster is sepearate patterns for 8 and 11 are used, as the pattern for 0 is very large
    if (len(m) == 24) and (m[:8] in sepPattern[0]) and (m[8:24] in sepPattern[1]):
    #if m in pattern:
       valid = True
    
    print(m, valid)

    if valid:
        validCount += 1

lengths = list(set(lengths))
lengths.sort()

print(f"Task 1: {validCount} messages are valid")