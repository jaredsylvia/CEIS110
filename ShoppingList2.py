# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:41:36 2021

@author: jared
"""
import matplotlib.pyplot as plt

def addItem():
    shoppingList = {'item' : [], 'qty' : [], 'price' : [], 'total' : []}
    while True:
        appendingItem = input('Item: ')
        if appendingItem == 'done':
            return(shoppingList)
        itemQty = int(input('Quantity: '))
        itemPrice = float(input('Unit price: '))
        shoppingList['item'].append(appendingItem)
        shoppingList['qty'].append(itemQty)
        shoppingList['price'].append(itemPrice)
        shoppingList['total'].append(itemPrice * itemQty)
       
def getTotals(val): 
    return val['total']    



print('Create and display a shopping list.')
print('Enter done for name of last item on list.')

shoppingList = addItem();

plt.pie(shoppingList['total'], labels = shoppingList['item'], startangle=45, shadow = True, autopct = '%1.0f%%')
plt.title('Allocation of your $' + str(sum(shoppingList['total'])))
plt.show()

plt.pie(shoppingList['qty'], labels = shoppingList['item'], startangle=45, shadow = True, autopct = '%1.0f%%')
plt.title('Total Individual Items')
plt.show()

print('Shopping List:')
for i in range(len(shoppingList['item'])):
    print(shoppingList['item'][i], ':', str(shoppingList['qty'][i]), 'at', str(shoppingList['price'][i]), 'each.')
    
        





    

