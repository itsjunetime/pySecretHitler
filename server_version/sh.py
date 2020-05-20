from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import random
import os
import shutil
import utils
import je

os.system('cls' if os.name == 'nt' else 'clear')
rows = shutil.get_terminal_size((100, 25))[1]
columns = shutil.get_terminal_size((100, 25))[0]

def printCentered(str):
    print(' '*int((columns - len(str)) / 2) + str)
    

def getPlayers():
    questions = [
        {
            'type': 'input',
            'name': 'playerName',
            'message': 'Inpur a new player name (input \'quit\' when done)',
        }
    ]

    players = []

    newPlayer = prompt(questions)
    while newPlayer['playerName'] != 'quit':
        if newPlayer['playerName'] not in players and len(newPlayer['playerName']) != 0:
            players.append(newPlayer['playerName'])
        elif newPlayer['playerName'] in players:
            print('%s is already in the game. Please choose a new one.' % newPlayer['playerName'])
        elif len(newPlayer['playerName']) == 0:
            print('Please enter a name or quit')
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
        print('\n')
        printCentered('All right, then get ready to play!')
    else:
        print('\n')
        printCentered('Sucks, \'cause I don\'t want to write them all down right now!')

def printDetails():
    numLines = 28
    deck = je.getValue('deck')

    os.system('cls' if os.name == 'nt' else 'clear')

    deck_display = utils.tcolors.blue + 'deck: [ '
    for i in deck:
        deck_display += '# '
    for i in range(je.getValue('num_total_cards') - len(deck)):
        deck_display += '_ '
    deck_display += ']'

    discard = je.getValue('discard')

    discard_display = utils.tcolors.green + 'discard: [ '
    for i in discard:
        discard_display += '# '
    for i in range(je.getValue('num_total_cards') - len(discard)):
        discard_display += '_ '
    discard_display += ']'

    firstLine = deck_display + ' '*int(int(columns) / 2 - len(deck_display)) + discard_display
    print(firstLine)
        

printDetails()
# print(int((rows - len(str)) / 2))
