#!/bin/env python3
from enum import Enum

class tcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        WHITE = '\033[37m'

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

cardWidth = 13 #Find another way to make this dynamic
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

