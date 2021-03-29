# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 12:38:54 2021

@author: jared
"""
shoppingList = []
itemAdding = 1
def addItem():
    global shoppingList
    appendingItem = input('Item: ')
    if appendingItem:
        shoppingList.append(appendingItem)
        return(1)
    else:
        global itemAdding
        itemAdding = 0
        return(0)
    

def printList():
    print('Your shopping list:')
    for u in shoppingList:
        print("{}. {}".format(int(shoppingList.index(u) + 1), u))
    return

print('Create and display a shopping list.')
print('Press enter on blank line to finish.')

while itemAdding == 1:
    addItem()

printList()





    

