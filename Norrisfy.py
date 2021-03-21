# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 12:16:55 2021

@author: jared
"""
import requests
import json
norrisfyMe = 'Y'

def norrisfy(fName, lName):
    norrisJoke = json.loads(json.dumps(requests.get('https://api.chucknorris.io/jokes/random').json()))['value']
    norrisified = norrisJoke.replace('Chuck', fName)
    norrisified = norrisified.replace('CHUCK', fName)
    norrisified = norrisified.replace('chuck', fName)
    norrisified = norrisified.replace('Norris', lName)
    norrisified = norrisified.replace('NORRIS', lName)
    norrisified = norrisified.replace('norris', lName)
    return norrisified


while norrisfyMe == 'Y' or norrisfyMe == 'y':
    firstName = input('First Name: ')
    lastName = input('Last Name: ')
    print(norrisfy(firstName, lastName))
    norrisfyMe = input("Again? (Y/N)")


    