# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 1:45:45 2021
Prime Number Generator
@author: jared
"""
import math

userNumRange = [0,0]
primeNums = []
print('\x1b[0;37;40m', 'Prime Number Generator')
while userNumRange[0] <= 0:
    try:
        userNumRange[0] = int(input('Choose a starting number: '))
        if userNumRange[0] <= 0:
            print('\x1b[7;30;41m', 'ERROR: Selected number must be a positive integer.', '\x1b[0;37;40m') 
    except ValueError:
        print('\x1b[7;30;41m', 'ERROR: Selected number must be a positive integer.', '\x1b[0;37;40m') 
        
while userNumRange[1] <= userNumRange[0]:
    try:
        userNumRange[1] = int(input('Choose a second number greater than the first: '))
        if userNumRange[1] <= userNumRange[0]:
            print('\x1b[7;30;41m', 'ERROR: Selection must be an integer and greater than starting number.', '\x1b[0;37;40m')
    except ValueError:    
            print('\x1b[7;30;41m', 'ERROR: Selection must be an integer and greater than starting number.', '\x1b[0;37;40m')

for i in range(userNumRange[0],userNumRange[1]):
    if all(i%u!=0 for u in range(2,int(math.sqrt(i))+1)):
        primeNums.append(i)


print('Prime Numbers:')
print('\x1b[3;32;40m', primeNums, '\x1b[0;37;40m')
    
