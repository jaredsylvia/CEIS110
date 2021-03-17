# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 12:30:45 2021
Number Counter
@author: jared
"""
evenNums = 0
oddNums = 1
print('Even Numbers:')
while (evenNums <= 100):
    if evenNums == 100:
        print(evenNums)
    elif evenNums < 100:
        print(evenNums, end=",")
    evenNums += 2
print('Odd Numbers:')
while (oddNums <= 100):
    if oddNums == 99:
        print(oddNums)
    elif oddNums < 99:
        print(oddNums, end=",")
    oddNums += 2
userNumsBegin = int(input('Choose a starting number: '))
userNumsEnd = int(input('Choose an end number: '))
userNumsIncrement = int(input('Choose an increment: '))
userNumsCurrent = userNumsBegin
print('User Defined Numbers:')
while (userNumsCurrent in range(userNumsBegin,userNumsEnd,userNumsIncrement)):
    nextNum = userNumsCurrent + userNumsIncrement
    if nextNum not in range(userNumsBegin,userNumsEnd,userNumsIncrement):
        print(userNumsCurrent)
    else:
        print(userNumsCurrent, end =",")
    userNumsCurrent += userNumsIncrement

    
