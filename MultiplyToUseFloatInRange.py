# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 23:28:50 2021

@author: jared
"""

def funcA(a):
    a = a * 10
    return(a)

def funcB(b):
    b = b * 10
    return(b)
        
#whichever dataset this represents holds floats as n.n
aInput = float(input("A float between .1 and 1 for funcA:"))
bInput = float(input("A float between .1 and 10 for funcB:"))
rangeStep = float(input("This is the number you'd like to step by between 0.1 and 1:"))


rangeStart = funcA(aInput)
rangeEnd = funcB(bInput)
rangeStep = rangeStep * 10

print('**Range multiplied to count integers**')
print('Range start:', str(rangeStart))
print('Range end:', str(rangeEnd))
print('Range step:', str(rangeStep))
print('**Range divided in loop to show floats**')

for x in range(int(rangeStart),int(rangeEnd),int(rangeStep)):
    print(x/10)
    