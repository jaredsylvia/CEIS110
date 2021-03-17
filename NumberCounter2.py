# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 12:30:45 2021
Number Counter
@author: jared
"""

evenNums = []
oddNums = []
userNums = []
userNumRange = [0,0,0]

for i in range(1,101):
    if (i % 2) == 0:
        evenNums.append(i)
    elif (i % 2) != 0:
        oddNums.append(i)
print('Even Numbers:')        
print(evenNums)
print('Odd Numbers:')
print(oddNums)

userNumRange[0] = int(input('Choose a starting number: '))        
userNumRange[1] = int(input('Choose an end number: '))
userNumRange[2] = int(input('Choose an increment: '))

for u in range(userNumRange[0],userNumRange[1],userNumRange[2]):
    userNums.append(u)

print('User Defined Numbers:')
print (userNums)

    
