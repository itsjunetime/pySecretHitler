#!/bin/env python3
from enum import Enum

class tcolors:
        purple = '\033[95m'
        blue = '\033[94m'
        green = '\033[92m'
        yellow = '\033[93m'
        red = '\033[91m'
        normal = '\033[0m'
        bold = '\033[1m'
        underline = '\033[4m'
        white = '\033[37m'

class actions:
        cards = 'cards'
        murder = 'murder'
        veto = 'veto'
        view = 'view'
        end = 'end'
        election = 'election'
        none = 'none'

# Enum('actions', 'cards murder veto view end election none')

blankCard = ("""
┌───────────┐
│           │
│           │
│           │
│           │
│           │
│           │
│           │
└───────────┘
""")

playedLiberalCard = ("""
┌───────────┐
│           │
│  █        │
│  █        │
│  █        │
│  █        │
│  ██████   │
│           │
└───────────┘
""")

liberalEndCard = ("""
┌───────────┐
│           │
│  ███ ███  │
│ █████████ │
│  ███████  │
│    ███    │
│     █     │
│           │
└───────────┘
""")

playedFascistCard = ("""
┌───────────┐
│           │
│  ██████   │
│  █        │
│  ████     │
│  █        │
│  █        │
│           │
└───────────┘
""")

fascistEndCard = ("""
┌───────────┐
│           │
│  ███ ███  │
│ ██ ███ ██ │
│  ███ ███  │
│   █████   │
│   █ █ █   │
│           │
└───────────┘
""")

fascistVetoCard = ("""
┌───────────┐
│ President │
│ may       │
│ murder a  │
│ player.   │
│ Gov has   │
│ veto      │
│ power.    │
└───────────┘
""")

fascistMurderCard = ("""
┌───────────┐
│           │
│ President │
│ may       │
│ murder a  │
│ player    │
│           │
│           │
└───────────┘
""")

fascistViewCard = ("""
┌───────────┐
│           │
│ President │
│ may view  │
│ a player's│
│ party     │
│ card      │
│           │
└───────────┘
""")

fascistPeekCard = ("""
┌───────────┐
│           │
│ President │
│ may view  │
│ the top   │
│ 3 cards   │
│           │
│           │
└───────────┘
""")

fascistElectionCard = ("""
┌───────────┐
│           │
│ President │
│ may choose│
│ the next  │
│ president │
│           │
│           │
└───────────┘
""")

cardWidth = len(blankCard.split('\n')[1]) #Find another way to make this dynamic
cardHeight = blankCard.count('\n')


def checkIfAction(numFascists, numPlayers, lastAction):
    fascistsPlayed = numFascists
    if fascistsPlayed == 5 and lastAction != 'veto':
        return 'veto'
    elif fascistsPlayed == 6:
        return 'end'
    if numPlayers < 7:
        if fascistsPlayed < 3:
            return 'none'
        elif fascistsPlayed == 3 and lastAction != 'cards':
            return 'cards'
        elif fascistsPlayed == 4 and lastAction != 'murder':
            return 'murder'
    elif numPlayers < 9:
        if fascistsPlayed < 2:
            return 'none'
        elif fascistsPlayed == 2 and lastAction != 'view':
            return 'view'
        elif fascistsPlayed == 3 and lastAction != 'cards':
            return 'cards'
        elif fascistsPlayed == 4 and lastAction != 'murder':
            return 'murder'
    else:
        if fascistsPlayed == 1 and lastAction != 'view1':
            return 'view1'
        elif fascistsPlayed == 2 and lastAction != 'view':
            return 'view'
        elif fascistsPlayed == 3 and lastAction != 'election':
            return 'election'
        elif fascistsPlayed == 4 and lastAction != 'murder':
            return 'murder'
    return 'none'

def getCard(name):
    if name == 'blank':
        return blankCard
    elif name == 'fascist':
        return playedFascistCard
    elif name == 'liberal':
        return playedLiberalCard
    elif name == 'fascist_end':
        return fascistEndCard
    elif name == 'liberal_end':
        return liberalEndCard
    elif name == 'veto':
        return fascistVetoCard
    elif name == 'murder':
        return fascistMurderCard
    elif name == 'loyalty':
        return fascistViewCard
    elif name == 'election':
        return fascistElectionCard
    elif name == 'peek':
        return fascistPeekCard
    else:
        print("yeah something went wrong my guy.")
