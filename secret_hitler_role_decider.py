#!/usr/bin/env python3

import random

def chooseHitler(playerArray):
    players = playerArray
    if len(players) < 5:
        quit("You have too few players to play this game. Exiting...")

    num_bad: int = int((len(players) - 3) / 2)
    if num_bad == -1:
        print("You have too few players to play this game.")

    hitler = random.randint(0, len(players) - 1)
    return hitler

def chooseFascists(players, hitler):
    fascists = []

    num_bad: int = int((len(players) - 3) / 2)

    for num in range(0, num_bad):
        newFascist = random.randint(0, len(players) - 1)
        while newFascist == hitler or players[newFascist] in fascists:
            newFascist = random.randint(0, len(players) - 1)
        else:
            fascists.append(newFascist)
    
    return fascists
