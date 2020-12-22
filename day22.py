#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 07:36:56 2020

@author: marc
"""
def readInitial():
    with open("input-day22", 'r') as f:
        lines = list(f.read().splitlines())
        
    p1 = []
    p2 = []
    l = lines[1]
    i = 1
    while (l != ''):
        p1.append(int(l))
        i += 1
        l = lines[i]
    i += 2
    l = lines[i]
    while (i < len(lines)-1):
        p2.append(int(l))
        i += 1
        l = lines[i]
    p2.append(int(l))
    
    return p1, p2

p1, p2 = readInitial()
count = 0
while not(len(p1) == 0 or len(p2) == 0):
    if count == 100000:
        print("Stopped game after 1000 rounds")
        break
    count += 1
    c1 = p1.pop(0)
    c2 = p2.pop(0)
    
    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    else:
        p2.append(c2)
        p2.append(c1)

def calcScore(opwin):
    pwin = opwin.copy()
    score = 0
    weight = len(pwin)
    while len(pwin) > 0:
        score += pwin.pop(0)*weight
        weight -= 1
    return score

if (len(p1) == 0):
    winner = 2
    score = calcScore(p2)
else:
    winner = 1
    score = calcScore(p1)
    
print(f"Task 1: Player {winner} wins after {count} rounds with score {score}.")
print()

c1list = []
c2list = [
        ]
def play(p1, p2, reclvl):
    print(f"=== Game {reclvl+1} ===")
    print()
    winner = 0
    count = 0
    cardConfigs1 = []
    cardConfigs2 = []
    while not(len(p1) == 0 or len(p2) == 0):
#        print(cardConfigs1)
#        print(cardConfigs2)
        print(f"-- Round {count+1} (Game {reclvl+1}) --")
        print(f"Player 1's deck: {[p for p in p1]}") 
        print(f"Player 2's deck: {[p for p in p2]}")
        if p1 in cardConfigs1:
            winner = 1
            break
        elif p2 in cardConfigs2:
            winner = 2
            break
        else:
            cardConfigs1.append(p1.copy())
            cardConfigs2.append(p2.copy())
            
            c1 = p1.pop(0)
            c2 = p2.pop(0)
            c1list.append(c1)
            c2list.append(c2)
            print(f"Player 1 plays {c1}")
            print(f"Player 2 plays {c2}")
            
            if len(c1list) == 185:
                print("stop!")
            
            if len(p1) >= c1 and len(p2) >= c2:
                print("Playing a sub-game to determine the winner...")
                print()
                rwin = play(p1[:c1], p2[:c2], reclvl+1)
                if rwin == 1:
                    p1.append(c1); p1.append(c2)
                else:
                    p2.append(c2); p2.append(c1)
            else:
                if c1 > c2:
                    rwin = 1
                    p1.append(c1)
                    p1.append(c2)
                else:
                    rwin = 2
                    p2.append(c2)
                    p2.append(c1)
                    
            print(f"Player {rwin} wins round {count+1} of game {reclvl+1}!")
            print()
            
            count += 1
    if len(p1) == 0:
        winner = 2
        score = calcScore(p2)
    elif len(p2) == 0:
        winner = 1
        score = calcScore(p1)
    else: 
        print(f"Game stopped by infinite loop rule: {p1 in cardConfigs1, p2 in cardConfigs2}, winner={winner}")
        if winner == 1:
            score = calcScore(p1)
        elif winner == 2:
            score = calcScore(p2)
    print(f"The winner of game {reclvl+1} is player {winner}!")
    if reclvl == 0:
        print("\n== Post-game results ==")
        print(f"Player 1's deck: {[p for p in p1]}")
        print(f"Player 2's deck: {[p for p in p2]}")
        print(f"The winner's score: {score}\n")
        print("Done!")
    else:
        print(f"\nAnyway, back to game {reclvl-1+1}\n")
    return winner
                    
p1, p2 = readInitial()
play(p1, p2, 0)            
                
