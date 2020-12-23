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
        prev = ListNode(olist[-1], None)
        self.nodedict = dict()
        self.valdict = dict()
        for i in range(len(olist)-2,0,-1):
            prev = ListNode(olist[i], prev)
            self.nodedict[i] = prev
            self.valdict[i] = olist[i]
        self.head = ListNode(olist[0], prev)
        self.length = len(olist)
        self.tail = self.getTail()
        if cyclic:
            self.tail.succ = self.head
        
    
    def getByVal(self, value, returnIndex=False):
        node = self.head
        count = 0
        while(node.val != value):
            if node.succ == None or count > self.length:
                return None
            else:
                node = node.succ
            count += 1
        if returnIndex:
            return (node, count)
        else: 
            return node
    
    def getByIdx(self, index, count=1, returnIdx=False, returnPreviousNode=False):
        node = self.head
        i = 0
        while i < index-1:
            node = node.succ
            i += 1
        if index == 0:
            prevNode = self.tail
        else:
            prevNode = node
            node = node.succ
            i += 1
        if count == 1:
            if returnPreviousNode:
                return (node.val, prevNode)
            else:
                if returnIdx:
                    return (node.val, i)
                else:
                    return node.val
        else:
            vals = [node.val]
            for _ in range(count-1):
                node = node.succ
                vals += [node.val]
            if returnPreviousNode:
                return (vals, prevNode)
            else:
                return vals
    
    def popByIdx(self, index, count=1):
        returnval, prevNode = self.getByIdx(index, count, returnPreviousNode=True) 
        nextNode = prevNode.succ
        for _ in range(count):
            nextNode = nextNode.succ
        prevNode.succ = nextNode
        self.length -= count
        if self.head.val in (returnval if type(returnval) == list else [returnval]):
            while self.head != nextNode:
                self.head = self.head.succ
        return returnval
    
    def indexOf(self, value):
        return self.getByVal(value, True)[1]
    
    def getTail(self):
        node = self.head
        counter = 0
        while node.succ != None and counter < self.length-1:
            node = node.succ
            counter += 1
        return node
    
    def insertAfterVal(self, afterval, insertlist):
        after = self.getByVal(afterval)
        tmpsucc = after.succ
        newlist = LinkedList(insertlist)
        after.succ = newlist.head
        newlist.tail.succ = tmpsucc
        self.length += len(insertlist)
    
    def getAll(self):
        allvals = []
        node = self.head
        for _ in range(self.length):
            allvals.append(node.val)
            node = node.succ
        return allvals
    
    def __str__(self):
        return str(self.getAll()) 
        
        
#inp = "284573961"
inp = "389125467"

ncups = 1000000
cups = [int(i) for i in inp]
#cups += list(range(max(cups)+1, ncups+1))
cups = LinkedList(cups, cyclic=True)
ncups = cups.length

nrmoves = 10
curcup = int(inp[0])
nextcup = int(inp[1])
curidx = 0
nextidx = 1
npick = 3 # number of cups to pick up

for i in range(nrmoves):
    if i % 10 == 0:
        print(f"move {i}...")
    
    print(cups)    
    pick = cups.popByIdx(nextidx, npick)
    print(pick)
    
    dest = curcup - 1
    while (dest in pick) or (dest == 0):
        if dest == 0:
            dest = ncups
        else:
            dest -= 1    
    print(curcup, dest)

    cups.insertAfterVal(dest, pick)
    
    curcup, curidx = cups.getByIdx(curidx+1, returnIdx=True)
    nextidx = curidx + 1
    
if cups.length < 20:
    print(); print(cups); print()
    output = ""
    for c in cups.getAll():
        output += str(c)
    output = output[output.index('1')+1:] + output[:output.index('1')]
    print(output)

label1 = cups.getByIdx(cups.indexOf(1) + 1)
label2 = cups.getByIdx(cups.indexOf(1) + 2)

print(f"Task 2: Stars are under cups {label1} and {label2}. Product is {label1*label2}")

