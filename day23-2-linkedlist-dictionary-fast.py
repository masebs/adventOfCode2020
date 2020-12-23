#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:19:31 2020

@author: marc.schneider
"""

class ListNode:
    def __init__(self, val, succ):
        self.val = val
        self.succ = succ
    
class LinkedList:
    def __init__(self, olist, cyclic=False):
        self.valdict = dict()
        prev = ListNode(olist[-1], None)
        self.valdict[olist[-1]] = prev
        for i in range(len(olist)-2,0,-1):
            prev = ListNode(olist[i], prev)
            self.valdict[olist[i]] = prev
        self.head = ListNode(olist[0], prev)
        self.valdict[olist[0]] = self.head
        self.length = len(olist)
        self.tail = self.getTail()
        if cyclic:
            self.tail.succ = self.head
        
    def getNodeByVal(self, value):
        return self.valdict[value]
    
    def popByVal(self, value, count=1):
        prevNode = self.valdict[value]
        nextNode = prevNode.succ
        vals = [nextNode.val]
#        del self.valdict[nextNode.val] # not really necessary to delete them as they will be overwritten on insert 
        for k in range(count-1):        # (and nothing happens in between, for this task at least)
            nextNode = nextNode.succ
            vals.append(nextNode.val)
#            del self.valdict[nextNode.val]
        nextNode = nextNode.succ
        prevNode.succ = nextNode
        self.length -= count
        if self.head.val in vals: # correct head if the old one was removed
            while self.head != nextNode:
                self.head = self.head.succ
        return vals
        
    def insertAfterVal(self, afterval, insertlist):
        after = self.getNodeByVal(afterval)
        tmpsucc = after.succ
        newlist = LinkedList(insertlist)
        after.succ = newlist.head
        newlist.tail.succ = tmpsucc
        self.length += len(insertlist)
        nextnode = after
        for k,i in enumerate(insertlist):
            nextnode = nextnode.succ
            self.valdict[i] = nextnode
            
    def getTail(self):
        node = self.head
        counter = 0
        while node.succ != None and counter < self.length-1:
            node = node.succ
            counter += 1
        return node
    
    def getAll(self):
        allvals = []
        node = self.head
        for _ in range(self.length):
            allvals.append(node.val)
            node = node.succ
        return allvals
    
    def __str__(self):
        return str(self.getAll()) 
        
        
inp = "284573961"
#inp = "389125467"

ncups = 1000000
cups = [int(i) for i in inp]
cups += list(range(max(cups)+1, ncups+1))
cups = LinkedList(cups, cyclic=True)
ncups = cups.length

nrmoves = 10000000
curcup = int(inp[0])
nextcup = int(inp[1])
#curidx = 0
nextidx = 1
npick = 3 # number of cups to pick up

ll = LinkedList([3, 8, 9, 1, 2, 5, 4, 6, 7], cyclic=True)

for i in range(nrmoves):
    if i % 1000000 == 0:
        print(f"move {i}...")
    
#    print(cups)    
    pick = cups.popByVal(curcup, npick)
#    print(pick)
    
    dest = curcup - 1
    while (dest in pick) or (dest == 0):
        if dest == 0:
            dest = ncups
        else:
            dest -= 1    
#    print(curcup, dest)

    cups.insertAfterVal(dest, pick)
    
    curcup = cups.getNodeByVal(curcup).succ.val
    
if cups.length < 20:
    print(); print(cups); print()
    output = ""
    for c in cups.getAll():
        output += str(c)
    output = output[output.index('1')+1:] + output[:output.index('1')]
    print(output)

label1 = cups.getNodeByVal(1).succ.val
label2 = cups.getNodeByVal(1).succ.succ.val

print(f"Task 2: Stars are under cups {label1} and {label2}. Product is {label1*label2}")

