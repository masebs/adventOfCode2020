#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 06:01:24 2020

@author: marc
"""

with open("input-day16", 'r') as f:
    lines = list(f.read().splitlines())

lit = iter(lines)
l = next(lit)
rules = []

while (l != ''):
    rules.append(l)
    l = next(lit)

next(lit)
myticket = next(lit)
myticket = [int(i) for i in myticket.split(',')]
next(lit); next(lit)
l  = next(lit)

tickets = []
while (l != ''):
    tickets.append(l)
    l = next(lit)

ruledict = {}
rulelist = []
for r in rules:
    name, rhs = r.split(': ')
    rhs1, rhs2 = rhs.split(' or ')
    ruledict[name] = [[int(i) for i in rhs1.split('-')], [int(i) for i in rhs2.split('-')]]
    rulelist.append([int(i) for i in rhs1.split('-')])
    rulelist.append([int(i) for i in rhs2.split('-')])

validFrom = min([r[0] for r in rulelist])
validTo = max([r[1] for r in rulelist])

for i, t in enumerate(tickets):
    tickets[i] = [int(k) for k in t.split(',')]

invalidValueSum = 0
invalidTickets = []
for t in tickets:
    for i in t:
        if not (validFrom <= i <= validTo):
            invalidValueSum += i
            invalidTickets.append(t)
        
print(f"Task 1: Invalid value sum is {invalidValueSum}")

print(f"  ... removing {len(invalidTickets)} invalid tickets from {len(tickets)} in total")
for t in invalidTickets:
    tickets.remove(t)
    
### Get values from all tickets for one field, then check rule by rule for these values whether they are fulfilled,
### and then look for a unique mapping from the lists of fulfilled rules

validDict = {} # will contain the valid columns for each rule
for rd in ruledict.keys(): 
    validDict[rd] = [] # initialize with empty lists
    
for i in range(len(tickets[0])):    # go through columns 
    vals = [t[i] for t in tickets]  # all values from this columns
    for rd in ruledict.keys():      # check for each rule whether the current column fulfills it
        r = ruledict[rd]
        if ((r[0][0] <= min(vals)) and (max(vals) <= r[1][1])): # are all vals between the outer bounds?
            forbiddenRange = list(range(r[0][1]+1, r[1][0]))
            if not any([v in forbiddenRange for v in vals]):    # are any vals in the forbidden range in between?
                validDict[rd].append(i)  # add this column to the list of valid columns for this rule

mapping = {} # now we need to find a unique mapping from the validDict - let's hope there is one
while (len(mapping.keys()) < len(validDict.keys())): # repeat until we have a complete mapping
    for v in validDict.keys():          # go through rules
        if (len(validDict[v]) == 1):    # if this rule if fulfilled by exactly one column, we have match
            foundval = validDict[v][0]  
            mapping[v] = foundval       # add to our mapping
            for rv in validDict.keys(): # remove this column from all other entries in validDict
                if (foundval in validDict[rv]):
                    validDict[rv].remove(foundval)

result = myticket[mapping['departure location']] * myticket[mapping['departure station']] * myticket[mapping['departure platform']] \
            * myticket[mapping['departure track']] * myticket[mapping['departure date']] * myticket[mapping['departure time']]
            
print(f"Task 2: Required product of my ticket's values is {result}")

