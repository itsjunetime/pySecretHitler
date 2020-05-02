#!/bin/env python

from __future__ import print_function, unicode_literals
from PyInquirer import prompt
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
previousGov = {'president': str(), 'chancellor': str()} # This will be ints to reference the player array. It references the previous government until the new chancellor is elected, then it references them until the next chancellor is elected.

currentPres = -1 # References players array. Starts at -1 since it is incremented immediately.
selectedCards = [0, 0, 0]
cardAnnouncement = "The card that has been played is..."
lastAction = ''

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
        if newPlayer['playerName'] not in players and len(newPlayer['playerName']) != 0:
            players.append(newPlayer["playerName"])
        elif newPlayer['playerName'] in players:
            print('%s is already in the game. Please choose a new one' % newPlayer['playerName'])
        elif len(newPlayer['playerName']) == 0:
            print('Please enter a name or quit.')
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

def nominateChancellor(isSpecialElection):

    chancellorChooser  = [
        {
            'type': 'input',
            'name': 'chancellor',
            'message': 'Type in the name of the chancellor that you chose:',
        }
    ] 

    newChancellor = prompt(chancellorChooser)['chancellor']
    
    while newChancellor not in players or newChancellor == previousGov['chancellor'] or newChancellor == previousGov['president'] or newChancellor == players[currentPres]:
        if newChancellor not in players:
            print("%s is not a player in the current game. Choose a new one." % newChancellor)
        else:
            if isSpecialElection is True:
                break
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
        previousGov['chancellor'] = newChancellor

        if fascistsPlayed >= 3:
            if newChancellor == hitler:
                print('Unfortunately, you just fell right into Hitler\'s trap. You elected Hitler as your chancellor. LIBERALS, you have lost! And FASCISTS, you have won!')
                input('Click any key when you are ready to quit.')
                quit(' '*int((columns - len('THANKS FOR PLAYING!')) / 2) + 'THANKS FOR PLAYING!')
            else:
                input('%s is NOT hitler! Be careful, though, they could still be a fascist. Press enter to continue...' % newChancellor)

        return True
    else:
        return False

def choosePolicies(selectedCards):
    cardWidth = sh_utils.cardWidth
    cardHeight = sh_utils.cardHeight

    input('Everybody close your eyes until only the current president is looking. President, once you are the only one with your eyes open, click enter.')

    cardsToShow = []
    cardSeparator = '     '
    numberSeparator = ' '*int(cardWidth + len(cardSeparator) - 2)
    policyCards = ("""""")
    marginFromSide = ((columns - (3 * cardWidth) - (2 * len(cardSeparator))) / 2)
    if selectedCards == [0, 0, 0]:
        for i in range(3):
            card = deck.pop(random.randint(0, len(deck) - 1))
            if card == pCards.f:
                cardsToShow.append(sh_utils.playedFascistCard)
            elif card == pCards.l:
                cardsToShow.append(sh_utils.playedLiberalCard)
    else:
        # print('entered else in choose policies')
        selectedCards.sort(reverse=True)
        for c in selectedCards:
            # print('c: ' + str(c))
            card = deck.pop(c)
            # print('card: ' + 'l' if card == pCards.l else 'f')
            if card == pCards.f:
                cardsToShow.append(sh_utils.playedFascistCard)
            elif card == pCards.l:
                cardsToShow.append(sh_utils.playedLiberalCard)
             

    print(' '*int(marginFromSide + (cardWidth / 2)) + '0' + numberSeparator + '1' + numberSeparator + '2')
    for i in range(cardHeight):
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
    
    input("President, hit enter FIRST, close your eyes, and then tell your chancellor to open their eyes.")
    os.system('cls' if os.name == 'nt' else 'clear')
    input("Chancellor, once you are the only one with your eyes open, hit enter.")

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
            'message': 'Select Card to Drop. If veto power has been enacted, you may select zero to propose a veto.',
            'name': 'drop',
            'choices': [
                {
                    'name': '0'
                },
                {
                    'name': '1'
                },
            ],
            'validate': lambda answer: "Please only choose one option" if len(answer) != 1 else True
        }
    ]

    secondRemoveCard = prompt(chanRemoveCard)['drop']
    while len(secondRemoveCard) != 1:
        if govHasVetoPower is True and len(secondRemoveCard) == 0:
            sureToVeto = [
                {
                    'type': 'confirm',
                    'name': 'veto',
                    'message': 'Ask the President if they would also like to veto. If they say yes, then you may veto. If no, you must choose. What did they say?'
                }
            ]

            presWantsVeto = prompt(sureToVeto)['veto']
            if presWantsVeto is True:
                return sh_utils.blankCard
            else:
                print('Veto failed.')
        print("Please select one, and only one option, to drop.")
        secondRemoveCard = prompt(chanRemoveCard)['drop']

    sRemoveCard = int(secondRemoveCard[0])

    discard.append(pCards.l if cardsToShow[sRemoveCard] == sh_utils.playedLiberalCard else pCards.f)
    del cardsToShow[sRemoveCard]
    selectedCards = [0, 0, 0]

    return cardsToShow[0]
                
def forcePlayCard():
    input("You have failed your election 3 times. A card will be force played. Click to continue.")
    if selectedCards == [0, 0, 0]:
        newCardNum = random.randint(0, len(deck) - 1)
    else:
        newCardNum = selectedCards[0]
        
    newCard = deck.pop(newCardNum)
    if newCard == pCards.f:
        fascistsPlayed += 1
        input(sh_utils.tcolors.FAIL + '\n\nThe card was a FASCIST!')
    else:
        liberalsPlayed += 1
        input(sh_utils.tcolors.OKBLUE + '\n\nThe card was a LIBERAL!')
    selectedCards[0] = random.randint(0, len(deck) - 1)

def murderPlayer(president):
    
    print("Due to the last fascist policy card that was passed, the current president must now kill a player.")
    murder = [
        {
            'type': 'input',
            'name': 'player',
            'message': 'Please type in the name of a character to murder.'
        }
    ]

    deadGuy = prompt(murder)['player']
    while deadGuy not in players or deadGuy == president:
        if deadGuy not in players:
            print('%s is not a real player. Please enter someone who is currently playing' % deadGuy)
        elif deadGuy == president:
            print('You cannot kill yourself. Choose again')
        deadGuy = prompt(murder)['player']
    
    players.remove(deadGuy)
    endStr = deadGuy + ' is now dead.'
    if deadGuy == hitler:
        endStr += ' They were HITLER. Good job liberals, you won!'
        print(endStr)
        input("Hit enter once you are ready to quit")
        print('\n\n' + ' '*int((columns - len('THANKS FOR PLAYING!')) / 2) + 'THANKS FOR PLAYING!')
        quit(' ')
    else:
        endStr += ' They were not Hitler. You do not know whether they were a fascist or a liberal.'
        print(endStr)
    
def previewCards():
    input('Everybody close your eyes except for the current president. President, hit a key once you are the only oen with your eyes open.')
    pCardsToShow = []
    outStr = 'The top 3 cards are a '
    for i in range(3):
        appendNum = random.randint(0, len(deck) - 1)
        while appendNum in pCardsToShow:
            appendNum = random.randint(0, len(deck) - 1)
        else:
            pCardsToShow.append(appendNum)
    for n, c in enumerate(pCardsToShow):
        selectedCards[n] = c
    # selectedCards = cardsToShow
    # for n, i in enumerate(pCardsToShow):
    for n, i in enumerate(selectedCards):
        if deck[i] == pCards.f:
            outStr += sh_utils.tcolors.FAIL + 'FASCIST' + sh_utils.tcolors.WHITE
        elif deck[i] == pCards.l:
            outStr += sh_utils.tcolors.OKBLUE + 'LIBERAL' + sh_utils.tcolors.WHITE
        if n == 0:
            outStr += ', a '
        elif n == 1:
            outStr += ', and a '
        else:
            outStr += '.'
    print(outStr)
    input('Hit enter when you have memorized these and are ready to continue')
    os.system('cls' if os.name == 'nt' else 'clear')

def viewLoyalty():
    playerChoice = [
       {
           'type': 'input',
           'name': 'loyalty',
           'message': 'Please choose whose loyalty you would like to view'
        }
    ]

    chosenPlayer = prompt(playerChoice)['loyalty']
    while chosenPlayer == players[currentPres] or chosenPlayer not in players:
        if chosenPlayer == players[currentPres]:
            print("You may not choose yourself")
        elif chosenPlayer not in players:
            print("%s is not an existing player." % chosenPlayer)
        chosenPlayer = prompt(playerChoice)['loyalty']

    input("Everybody close your eyes except for the current president. Click enter once everybody else has closed their eyes.")

    print("%s is a ....." % chosenPlayer)
    outStr = ' '*int((columns - len('LIBERAL')) / 2) # Since liberal and fascist have the same number of characters
    if chosenPlayer == hitler or chosenPlayer in fascists:
        outStr += sh_utils.tcolors.FAIL + 'FASCIST'
    else:
        outStr += sh_utils.tcolors.OKBLUE + 'LIBERAL'

    print(outStr)

def specialElection():
    newPres = [
        {
            'type': 'input',
            'name': 'president',
            'message': 'Current President, please choose who will be the next president. They can be anyone besides yourself; rules of eligibility do not apply in a special election.'
        }
    ]

    newPresident = prompt(newPres)['president']
    if newPresident == players[currentPres] or newPresident not in players:
        if newPresident == players[currentPres]:
            print('You cannot choose yourself. Please choose again.')
        if newPresident not in players:
            print('%s is not a real player. Please choose again.' % newPresident)
        newPresident = prompt(newPres)['president']
    
    input('%s, you are the new president. The regular order of government will continue once your turn is over. Hit enter to continue.')
    passed = nominateChancellor(True)
    if passed is True:
        previousGov['president'] = players[currentPres]
    else:
        failedElections += 1
        if len(deck) < 3:
            for i in discard:
                deck.append(i)
                discard.remove(i)
        if failedElections == 3:
            forcePlayCard()
        input("Press enter when you are ready to continue...")
        return
    
    cardToPlay = choosePolicies(selectedCards)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' '*int((columns - len(cardAnnouncement)) / 2) + cardAnnouncement)
    if cardToPlay == sh_utils.playedFascistCard:
        print('\n\n' + ' '*int((columns - len('FASCIST')) / 2) + sh_utils.tcolors.FAIL + 'FASCIST' + '\n\n\n')
        fascistsPlayed += 1
    else:
        print('\n\n' + ' '*int((columns - len('LIBERAL')) / 2) + sh_utils.tcolors.OKBLUE + 'LIBERAL' + '\n\n\n')
        liberalsPlayed += 1
    
    if sh_utils.checkIfAction(fascistsPlayed, numPlayers, lastAction) != 'none':
        action = sh_utils.checkIfAction(fascistsPlayed, numPlayers, lastAction)
        if action == 'cards':
            lastAction = 'cards'
            previewCards()
        elif action == 'murder':
            lastAction = 'murder'
            prevPresident = players[currentPres]
            murderPlayer(newPresident)
            currentPres = players.index(prevPresident) # To make sure that it increments correctly
        elif action == 'veto':
            lastAction = 'veto'
            prevPresident = players[currentPres]
            murderPlayer(newPresident)
            currentPres = players.index(prevPresident) # To make sure that it increments correctly
            print("The Government now has the power to veto.")
            govHasVetoPower = True
            input("Press enter when you are ready to continue...")
        elif action == 'view':
            lastAction = 'view'
            viewLoyalty()
        elif action == 'view1':
            lastAction = 'view1'
            viewLoyalty()
        elif action == 'end':
            if fascistsPlayed == 6:
                endStr = '\nThe ' + sh_utils.tcolors.FAIL + 'FASCISTS' + sh_utils.tcolors.WHITE + 'won. Great job, everyone!'
            elif liberalsPlayed == 5:
                endStr = '\nThe ' + sh_utils.tcolors.OKBLUE + 'LIBERALS' + sh_utils.tcolors.WHITE + 'won. Great job, everyone!'
            print(endStr)
            input('\n\nPress any key when you are ready to quit...')
        elif action == 'election':
            pass
        else:
            quit('Something went wrong. Talk to Ian.')
            
    # Leave this at the end of this loop
    input("Hit a key when you are ready to continue...")
    if len(deck) < 3:
        for i in discard:
            deck.append(i)
            discard.remove(i)
    
# Checking Terminal Dimensions

os.system('cls' if os.name == 'nt' else 'clear')
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
hitler = secret_hitler_role_decider.chooseHitler(players)
fascists = secret_hitler_role_decider.chooseFascists(players, hitler)

input('\nEverybody close your eyes except for %s. %s, keep your eyes open and hit enter once everyone else has their eyes closed.' % (players[0], players[0]))
for i in players:
    os.system('cls' if os.name == 'nt' else 'clear')
    playerLine = i + ', you are '
    playerLine += 'a ' if i != hitler else ''
    playerLine += sh_utils.tcolors.FAIL if i in fascists or i == hitler else sh_utils.tcolors.OKBLUE
    if i in fascists:
        playerLine += 'FASCIST. ' + sh_utils.tcolors.WHITE + 'Your objective is to get 6 fascist policies passed or elect Hitler as chancellor after 3 fascist cards are passed, all while remaining to appear liberal.'
    elif i == hitler:
        playerLine += 'HITLER. ' + sh_utils.tcolors.WHITE + 'Your objective is to get 6 fascist policies passed or to get elected as chancellor after 3 fascist cards are passed, all while remaining to appear liberal.'
    else:
        playerLine += 'LIBERAL. ' + sh_utils.tcolors.WHITE + 'Your objective is to get 5 liberal policies passed and prevent the dirty fascists from passing their policies or electing Hitler.'
    print(playerLine)
    if i != players[-1]:
        input('%s, please close your eyes and then hit enter and then tell %s to open their eyes. ' % (i, players[players.index(i) + 1]))
        os.system('cls' if os.name == 'nt' else 'clear')
        input('%s, once you are the only one with your eyes open, please press enter.' % players[players.index(i) + 1])
    else:
        input('%s, hit any key once you are ready to start the game' % i)

os.system('cls' if os.name == 'nt' else 'clear')

if numPlayers < 7:
    print('This next part requires some coordination. Everybody, close your eyes and nominate somebody to count to 20, but fascists and Hitler, reopen your eyes after 2 seconds.')
    print('Find the other fascists, identify them, then close your eyes once everybody has been identified. Reopen them once the nominated person has announced that they have reached 20 seconds. Or, if you don\'t like this, do it your own way.')
    input('Once everyone has their eyes back open, hit any key')
else:
    print('This next part requires some coordination. Everybody, stick out your fist, nominate somebody to count to 20, and close your eyes, but fascists EXCLUDING Hitler, reopen your eyes after 2 seconds.')
    print('Find the other fascists and identify them. Hitler, once everyone\'s eyes are closed, put out your thumb and wiggle it so that all the fascists can see.')
    print('Fascists, once you have identified yourselves and Hitler, close your eyes. Reopen them once the nominated person has announced that they have reached 20 seconds. Or, if you don\'t like this, do it your own way.')
    input('Once everyone has their eyes back open, hit any key')

os.system('cls' if os.name == 'nt' else 'clear')
askIfNeedInstructions()
printDetails()

while True: 
    currentPres = (currentPres + 1) % len(players)
    printDetails()
    print(sh_utils.tcolors.WHITE + "It is %s's turn as President. %s, nominate a Chancellor." % (players[currentPres], players[currentPres]))
    passed = nominateChancellor(False)
    if passed is True:
        previousGov['president'] = players[currentPres]
        failedElections = 0
    else:
        failedElections += 1
        if len(deck) < 3:
            for i in discard:
                deck.append(i)
                discard.remove(i)
        if failedElections == 3:
            forcePlayCard()
        input("Press enter when you are ready to continue...")
        continue
    
    cardToPlay = choosePolicies(selectedCards)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print(' '*int((columns - len(cardAnnouncement)) / 2) + cardAnnouncement)
    if cardToPlay == sh_utils.playedFascistCard:
        print('\n\n' + ' '*int((columns - len('FASCIST')) / 2) + sh_utils.tcolors.FAIL + 'FASCIST' + sh_utils.tcolors.WHITE + '\n\n\n')
        fascistsPlayed += 1
    elif cardToPlay == sh_utils.playedLiberalCard:
        print('\n\n' + ' '*int((columns - len('LIBERAL')) / 2) + sh_utils.tcolors.OKBLUE + 'LIBERAL' + sh_utils.tcolors.WHITE + '\n\n\n')
        liberalsPlayed += 1
    elif cardToPlay == sh_utils.blankCard:
        print('\n\n' + ' '*int((columns - len('VETOED')) / 2) + sh_utils.tcolors.OKGREEN + 'VETOED' + sh_utils.tcolors.WHITE + '\n\n\n')
    
    if sh_utils.checkIfAction(fascistsPlayed, numPlayers, lastAction) != 'none':
        action = sh_utils.checkIfAction(fascistsPlayed, numPlayers, lastAction)
        if action == 'cards':
            lastAction = 'cards'
            previewCards()
        elif action == 'murder':
            lastAction = 'murder'
            prevPresident = players[currentPres]
            murderPlayer(players[currentPres])
            currentPres = players.index(prevPresident) # To make sure that it will correctly increment at restart of the loop
        elif action == 'veto':
            lastAction = 'veto'
            prevPresident = players[currentPres]
            murderPlayer(players[currentPres])
            currentPres = players.index(prevPresident) # Since the number of players decreased by 1
            print("The Government now has the power to veto.")
            govHasVetoPower = True
            input("Press enter when you are ready to continue...")
        elif action == 'view':
            lastAction = 'view'
            viewLoyalty()
        elif action == 'view1':
            lastAction = 'view1'
            viewLoyalty()
        elif action == 'end':
            if fascistsPlayed == 6:
                endStr = '\nThe ' + sh_utils.tcolors.FAIL + 'FASCISTS' + sh_utils.tcolors.WHITE + 'won. Great job, everyone!'
            elif liberalsPlayed == 5:
                endStr = '\nThe ' + sh_utils.tcolors.OKBLUE + 'LIBERALS' + sh_utils.tcolors.WHITE + 'won. Great job, everyone!'
            print(endStr)
            input('\n\nPress any key when you are ready to quit...')
        elif action == 'election':
            lastAction = 'election'
            specialElection()
        else:
            quit('Action was %s. Something went wrong. Talk to Ian.' % action)
            
    # Leave this at the end of this loop
    input("Hit a key when you are ready to continue...")
    if len(deck) < 3:
        for i in discard:
            deck.append(i)
            discard.remove(i)

# except KeyboardInterrupt:
    # sureToQuit = input("Are you sure you want to quit? [y/n]")
    # while y not in sureToQuit and n not in sureToQuit:
        # print("Please input only 'y' or 'n'")
        # sureToQuit = input("Are you sure you want to quit? [y/n]")
    # else:
        # if y in sureToQuit:
            # quit('Thanks for playing')
        # else:
            # pass
