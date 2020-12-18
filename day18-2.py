#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 05:59:49 2020

@author: marc
"""

class opTree:
    def __init__(self, op):
        self.parent = None
        self.left = None
        self.right = None
        self.op = op
        
    def execute(self): # postorder traversal while executing operations
        if (self.op == None):
            print("ERROR: Empty node in tree!")
            return None
        elif (self.op in ['+', '*']): # we are an operator, i.e. not a leaf 
            l = self.left.execute()
            r = self.right.execute()
            if (self.op == '+'):
                return l + r
            else:
                return l * r
        else:               # we are a number, i.e. a leaf
            return self.op  # just return ourselves

with open("input-day18", 'r') as f:
    lines = list(f.read().splitlines())

result = 0

for l in lines:
    ## add brackets to assure correct precedence!
    # first, double all existing brackets
    insertPos = []
    for i in range(len(l)):
        if (l[i] == '('):
            insertPos.append([i,'('])
        elif (l[i] == ')'):
            insertPos.append([i,')'])
            
    for i, [p, c] in enumerate(insertPos):
        l = l[:p+i] + c + l[p+i:]
    
    # Append brackets at the begin and at the end
    l = '( ' + l
    l = l + ' )'
    
    # Replace * (which has lower precedence) with )*(
    i = 0
    while (i < len(l)):
        if (l[i] == '*'):
            l = l[:i] + ') * (' + l[i+1:]
            i += 4
        i += 1
    
    root = opTree(None)
    subtrees = []
    cur = root
    for ic,c in enumerate(l):
        if (c == ' '):
            continue
        elif (c == '('):
            while (not (cur.left == None or cur.right == None)) or (cur.parent != None): # go up to next node which has one child free
                cur = cur.parent
            subtrees.append(cur)
            cur = opTree(None)

        elif (c == ')'):
            while (cur.parent != None): # go to root of subtree
                cur = cur.parent 
            while (cur.op == None) and (cur.right == None): # This is if there is an unnecessary bracket around the expression
                cur = cur.left
            insertNode = subtrees.pop()
            cur.parent = insertNode
            if (insertNode.left == None):
                insertNode.left = cur
            else:
                insertNode.right = cur
            cur = insertNode
            
        elif (c in ['+', '*']):
            ## This could be the variant with lookahead, without string editing
            # nextop = ''
            # for lc in l[ic+1:]: # look for next operator ahead
            #     if (lc == '+'):
            #         nextop = '+'
            #         break
            #     elif (lc == '*'):
            #         nextop = '*'
            #         break
            # if (nextop == '+'): 
            #     # nextop is '+', which has high precedence -> save current operator and following operand for later,
            #     # and treat the next operation first!
            # else
            #     # nextop is *, which has low precedence, or there is no other op -> continue building optree as usual  
            while (cur.parent != None) and ((cur.parent.op != None) if cur.parent != None else False): # go up until we find a free node
                cur = cur.parent
            if (cur.op == None):   # found a free node
                cur.op = c
            else: # reached root -> create new root and add operator there
                newroot = opTree(c)
                cur.parent = newroot
                newroot.left = cur
                cur = newroot
                if (len(subtrees) == 0): # we are in main tree
                    root = newroot

        else: # Number
            n = opTree(int(c))
            if (cur.left == None):
                n.parent = cur
                cur.left = n
            elif (cur.right == None):
                n.parent = cur
                cur.right = n
            else:
                newCur = opTree(None)
                cur.parent = newCur
                newCur.left = cur
                cur = newCur
    
    while (root.op == None) and (root.right == None): # This is if there is an unnecessary bracket around the expression
        root = root.left
        
    result += root.execute()

print(f"Task 2: Sum is {result}")