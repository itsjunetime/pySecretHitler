#!/bin/env python

from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from enum import Enum
import random
import os
import shutil
import secret_hitler_role_decider
import sh_utils

players = []
fascists = []
pCards = Enum('pCards', 'f l')
deck = [pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.f, pCards.l, pCards.l, pCards.l, pCards.l, pCards.l, pCards.l]
discard = []

fascistsPlayed = 0
liberalsPlayed = 0
failedElections = 0
govHasVetoPower = False
previousGov = {'president': int(), 'chancellor': int()} # This will be ints to reference the player array. It references the previous government until the new chancellor is elected, then it references them until the next chancellor is elected.

currentPres = 0 # References players array

cardAnnouncement = "The card that has been played is..."

def getPlayers():
    questions = [
        {
            'type': 'input',
            'name': 'playerName',
            'message': 'Input a new player name (input \'quit\' when done)',
        }
    ]
    
    players = []

    newPlayer = prompt(questions)
    while newPlayer["playerName"] != "quit":
        players.append(newPlayer["playerName"])
        newPlayer = prompt(questions)

    return players

def askIfNeedInstructions():
    questions = [
        {
            'type': 'confirm',
            'message': 'Do you all know how to play the game already?',
            'name': 'known',
            'default': True,
        }
    ]

    knowRules = prompt(questions)
    if knowRules['known'] is True:
        print("All right, then get ready to play!")
    else:
        print("Sucks, cause I don't want to write them all down right now!!")

def printDetails():
    numLines = 28 # Increase this as you add more lines

    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Setting up deck
    deck_display = sh_utils.tcolors.OKBLUE + 'deck: [ '
    for i in deck:
        deck_display += '# '
    for i in range(17 - len(deck)):
        deck_display += '_  '
    deck_display += ']'

    # Setting up discard display
    discard_display = sh_utils.tcolors.OKGREEN + 'discard: [ '
    for i in discard:
        discard_display += '# '
    for i in range(17 - len(discard)):
        discard_display += '_ '
    discard_display += ']'

    # Printing the first line
    firstLine = deck_display + ' '*int(int(columns) / 2 - len(deck_display)) + discard_display
    print(firstLine)

    printFascistCards()

    printFailedElections()

    printLiberalCards()

    # Leave this always at the end
    print('\n'*int(rows-(numLines + 10)))

def printFascistCards():
    # Printing the fascist card section now
    print('\n' + sh_utils.tcolors.FAIL + ' '*int((columns - len('FASCISTS')) / 2) + 'FASCISTS')

    fascistString = (""" """)
    cardHeight = sh_utils.cardHeight
    cardWidth = sh_utils.cardWidth
    numCards = 6 # Can be 7 if you go extended
    cardSeparator = ' -> '
    cardsToPlay = []

    for f in range(fascistsPlayed):
        cardsToPlay.append(sh_utils.playedFascistCard)
    if numPlayers < 7:
        smallPlayerCards = (sh_utils.blankCard, sh_utils.blankCard, sh_utils.fascistPeekCard, sh_utils.fascistMurderCard, sh_utils.fascistVetoCard)
        for c in range(fascistsPlayed, numCards - 1): # do the - 1 cause we don't include endcard in the tuples
            cardsToPlay.append(smallPlayerCards[c]) 
    elif numPlayers < 9:
        mediumPlayerCards = (sh_utils.blankCard, sh_utils.fascistViewCard, sh_utils.fascistPeekCard, sh_utils.fascistMurderCard, sh_utils.fascistVetoCard)
        for c in range(fascistsPlayed, numCards - 1):
            cardsToPlay.append(mediumPlayerCards[c])
    else:
        largePlayerCards = (sh_utils.fascistViewCard, sh_utils.fascistViewCard, sh_utils.fascistElectionCard, sh_utils.fascistMurderCard, sh_utils.fascistVetoCard)
        for c in range(fascistsPlayed, numCards - 1):
            cardsToPlay.append(largePlayerCards[c])

    for i in range(cardHeight):
        totalLine = ' '*int((columns - ((numCards * cardWidth) + (len(cardSeparator) * (numCards - 1)))) / 2)
        currLineCardSeparator = cardSeparator if i == int((cardHeight) / 2)  else ' '*len(cardSeparator)
        for c in cardsToPlay:
            totalLine += c.splitlines()[i] + currLineCardSeparator
        totalLine += sh_utils.fascistEndCard.splitlines()[i]

        fascistString += totalLine + '\n'

    print(fascistString)

def printFailedElections():
    failDots = 4
    fTTitle = sh_utils.tcolors.WARNING + 'FAILURE TRACKER'
    print (' '*int((columns - len(fTTitle)) / 2) + fTTitle)
    fs = "Failures: "
    for i in range(failDots):
        if i == failedElections:
            fs += "● "
        else:
            fs += "○ "
        if i != failDots - 1:
            fs += "-▶ "
    fs += " A card will be overturned."

    print(' '*int((columns - len(fs)) / 2) + fs)

def printLiberalCards():
    print('\n' + sh_utils.tcolors.OKBLUE + ' '*int((columns - len('LIBERALS')) / 2) + 'LIBERALS')

    liberalString = (""" """)
    cardHeight = sh_utils.cardHeight
    cardWidth = sh_utils.cardWidth
    numCards = 5 # since it can be 6 if you play extended
    cardSeparator = ' -> '
    cardsToPlay = []
    for l in range(liberalsPlayed):
        cardsToPlay.append(sh_utils.playedLiberalCard)

    for c in range(liberalsPlayed, numCards - 1):
        cardsToPlay.append(sh_utils.blankCard)

    for i in range(cardHeight):
        totalLine = ' '*int((columns - ((numCards * cardWidth) + (len(cardSeparator) * (numCards - 1)))) / 2)
        currLineCardSeparator = cardSeparator if i == int((cardHeight) / 2) else ' '*len(cardSeparator)
        for c in cardsToPlay:
            totalLine += c.splitlines()[i] + currLineCardSeparator
        totalLine += sh_utils.liberalEndCard.splitlines()[i]

        liberalString += totalLine + '\n'

    print(liberalString)

def nominateChancellor():

    chancellorChooser  = [
        {
            'type': 'input',
            'name': 'chancellor',
            'message': 'Type in the name of the chancellor that you chose:',
        }
    ] 

    newChancellor = prompt(chancellorChooser)['chancellor']
    
    while newChancellor not in players or newChancellor == players[previousGov['chancellor']] or newChancellor == players[previousGov['president']] or newChancellor == players[currentPres]:
        if newChancellor not in players:
            print("%s is not a player in the current game. Choose a new one." % newChancellor)
        else:
            print("%s is not eligible to be chancellor. Choose a new one." % newChancellor)
        newChancellor = prompt(chancellorChooser)['chancellor']
    
    didTheyPass = [
        {
            'type': 'confirm',
            'message': 'Let the rest of the players choose now if they want this player as their chancellor. Did the appointment pass?',
            'name': 'passed',
            'default': True
        }
    ]

    passed = prompt(didTheyPass)['passed']
    if passed is True:
        previousGov['chancellor'] = players.index(newChancellor)
        return True
    else:
        return False


def choosePolicies():
    cardWidth = sh_utils.cardWidth
    cardHeight = sh_utils.cardHeight
    
    confirmPresEyes = [
        {
            'type': 'confirm',
            'name': 'onlyPresLooking',
            'message': 'Everybody close your eyes until only the current president is looking. President, once you are the only one with your eyes open, click enter.',
            'default': True
        }
    ]

    prompt(confirmPresEyes)
    cardsToShow = []
    cardSeparator = '     '
    numberSeparator = ' '*int(cardWidth + len(cardSeparator) - 2)
    policyCards = ("""""")
    marginFromSide = ((columns - (3 * cardWidth) - (2 * len(cardSeparator))) / 2)
    for i in range(3):
        card = deck.pop(random.randint(0, len(deck) - 1))
        if card == pCards.f:
            cardsToShow.append(sh_utils.playedFascistCard)
        elif card == pCards.l:
            cardsToShow.append(sh_utils.playedLiberalCard)
    
    print(' '*int(marginFromSide + (cardWidth / 2)) + '0' + numberSeparator + '1' + numberSeparator + '2')
    for i in range(cardHeight):
        # for c in cardsToShow:
            # policyCards += c.splitlines()[i]
        policyCards += ' '*int(marginFromSide)
        policyCards += cardsToShow[0].splitlines()[i] + cardSeparator
        policyCards += cardsToShow[1].splitlines()[i] + cardSeparator
        policyCards += cardsToShow[2].splitlines()[i] + '\n'
    print(policyCards)
    
    presRemoveCard = [
        {
            'type': 'checkbox',
            'qmark': '>',
            'message': 'Select Card to Drop',
            'name': 'drop',
            'choices': [
                {
                    'name': '0'
                },
                {
                    'name': '1'
                },
                {
                    'name': '2'
                }
            ],
            'validate': lambda answer: "Please only choose one option" if len(answer) != 1 else True
        }
    ]

    removeCard = prompt(presRemoveCard)['drop']
    while len(removeCard) != 1:
        print("Please pick one, and only one, card.")
        removeCard = prompt(presRemoveCard)['drop']

    firstRemoveCard = int(removeCard[0])

    discard.append(pCards.l if cardsToShow[firstRemoveCard] == sh_utils.playedLiberalCard else pCards.f)
    del cardsToShow[firstRemoveCard]
    
    confirmChanEyes = [
        {
            'type': 'confirm',
            'name': 'onlyChanLooking',
            'message': 'President, close your eyes and tell your chancellor to open their eyes. Chancellor, once you are the only one with your eyes open, hit enter.',
            'default': True,
        }
    ]

    prompt(confirmChanEyes)
    policyCards = ("""""")
    print(' '*int((columns - 2 - len(numberSeparator)) / 2) + '0' + numberSeparator + '1')
    for i in range(cardHeight):
        # for c in cardsToShow:
            # policyCards += c.splitlines()[i]
        policyCards += ' '*int((columns - (2 * cardWidth) - len(cardSeparator)) / 2)
        policyCards += cardsToShow[0].splitlines()[i] + cardSeparator
        policyCards += cardsToShow[1].splitlines()[i] + '\n'
    print(policyCards)

    chanRemoveCard = [
        {
            'type': 'checkbox',
            'qmark': '>',
            'message': 'Select Card to Drop',
            'name': 'drop',
            'choices': [
                {
                    'name': '0'
                },
                {
                    'name': '1'
                },
            ],
            'validate': lambda answer: "Please only choose one option" \
                    if len(answer) != 1 else True
        }
    ]

    secondRemoveCard = prompt(chanRemoveCard)['drop']
    while len(secondRemoveCard) != 1:
        print("Please select one, and only one option, to drop.")
        secondRemoveCard = prompt(chanRemoveCard)['drop']

    sRemoveCard = int(secondRemoveCard[0])

    discard.append(pCards.l if cardsToShow[sRemoveCard] == sh_utils.playedLiberalCard else pCards.f)
    del cardsToShow[sRemoveCard]

    return cardsToShow[0]
                
def forcePlayCard():
    input("You have failed your election 3 times. A card will be force played. Click to continue.")
    newCardNum = random.randint(0, len(deck) - 1)
    newCard = deck.pop(newCardNum)
    if newCard == pCards.f:
        fascistsPlayed += 1
        input(sh_utils.tcolors.FAIL + '\n\nThe card was a FASCIST!')
    else:
        liberalsPlayed += 1
        input(sh_utils.tcolors.OKBLUE + '\n\nThe card was a LIBERAL!')

# Checking Terminal Dimensions

os.system('cls' if os.name == 'nt' else 'clear') # This line is throwing invalid syntax; just run clear &&.
termsize = shutil.get_terminal_size((100, 25))
columns = termsize[0]
rows = termsize[1]
if columns < 100 or rows < 40:
    quit("Your window is currently %dx%d. Please make it larger than 100x40. Quitting..." % (columns, rows))

print("""
        WELCOME TO SECRET HITLER!
        Prepare to lie.
""")

print("You will now be asked to input the players. Please note that play will continue in the order that you input the characters.\n")

players = getPlayers()
numPlayers = len(players)
hitlerNum = secret_hitler_role_decider.chooseHitler(players)
fascistNums = secret_hitler_role_decider.chooseFascists(players, hitlerNum)
hitler = players[hitlerNum]
for f in fascistNums:
    fascists.append(players[f])

print('\n')

askIfNeedInstructions()
printDetails()

while True: # Commentin this out to stop an infinite loop for now
    printDetails()
    print("It is %s's turn as President. %s, nominate a Chancellor." % (players[currentPres], players[currentPres]))
    passed = nominateChancellor()
    if passed is True:
        previousGov['president'] = currentPres
    else:
        failedElections += 1
        if len(deck) < 3:
            for i in discard:
                deck.append(i)
                discard.remove(i)
        if failedElections == 3:
            forcePlayCard()
        currentPres += 1
        continue
    
    cardToPlay = choosePolicies()
    
    print(' '*int((columns - len(cardAnnouncement)) / 2) + cardAnnouncement)
    if cardToPlay == sh_utils.playedFascistCard:
        print('\n\n' + ' '*int((columns - len('FASCIST')) / 2) + sh_utils.tcolors.FAIL + 'FASCIST' + '\n\n\n')
        fascistsPlayed += 1
    else:
        print('\n\n' + ' '*int((columns - len('LIBERAL')) / 2) + sh_utils.tcolors.OKBLUE + 'LIBERAL' + '\n\n\n')
        liberalsPlayed += 1
    
    if sh_utils.checkIfAction(fascistsPlayed, numPlayers) == 'none':
        input("Hit a key when you are ready to continue...")
        currentPres += 1
        continue
    else:
        action = sh_utils.checkIfAction(fascistsPlayed, numPlayers)
        if action == 'cards':
            # Do action here
            pass
        elif action == 'murder':
            # Do action here
            pass
        elif action == 'veto':
            # Do action here
            pass
        elif action == 'view':
            # Do action here
            pass
        elif action == 'end':
            # Do action here
            pass
        elif action == 'election':
            # Do action here
            pass
        else:
            quit('Something went wrong. Talk to Ian.')
            
    # Leave this at the end of this loop
    input("Hit a key when you are ready to continue...")
    if len(deck) < 3:
        for i in discard:
            deck.append(i)
            discard.remove(i)
    currentPres += 1
