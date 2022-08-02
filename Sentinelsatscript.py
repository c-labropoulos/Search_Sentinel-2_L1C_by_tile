from collections import OrderedDict

import pyautogui as pyautogui
from past.builtins import raw_input
from sentinelsat import SentinelAPI
import getpass
print("Insert Credentials for Copernicus Open Access Hub ")
user = raw_input("Username:")
#print("Password for " + user + ":")
paswrd = pyautogui.password(text="Password for user " + str(user) + ":", title='Password', default='', mask='*')



api = SentinelAPI(user, paswrd)
def search(x,y,z,t,tiles):
    query_kwargs = {
        'cloudcoverpercentage': (float(x), float(y)),
        # "cloudcoverpercentage":'5',
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'date': (str(z), str(t))}

    products = OrderedDict()
    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)
    return products

def decide():
    print("Do you want to download all the products \t Y/N")
    dicision = input()
    if dicision == 'y' or dicision == 'Y':
        api.download_all(products)
    elif dicision == 'n' or dicision == 'N':
        print("Do you want to download one or only a specific amount of products\t Y/N")
        decision = input()
        if decision == 'y' or decision == 'Y':
            print("How many products do you want to download")
            prnum = input()
            if prnum.isnumeric() != True:
                print("Insert the NUMBER of products you want to download")
                prnum = input()
            for i in range(int(prnum)):
                print("Please provide the code of the product \nEXAMPLE OF CODE : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx ")
                code = str(input())
                api.download(code)
        elif decision == 'n' or decision == 'N':
            # print(products)

            print(*[str(k) + ':' + str(v) for k, v in products.items()], sep='\n')
    else:
        print("WRONG INPUT")

tiles = []
#https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59 find tiles from the map in the site
#34SEJ

print('How many  Tiles do you want to search for :')
t = input()
if t.isnumeric() != True:
    print("Insert the NUMBER of tiles you want to search for :")
    t = input()
t=int(t)
for i in range(t):
 print("Add  tile")
 y = input()
 tiles.append(str(y).upper())
 #print(tiles)

 #if input()=='y' or input()=='Y':
    #print('Enter Tile:')
    #y = input()
   # tiles.append(str(y))
print("The added tiles are :")
print(tiles)

print("What cloud percentage do you the product to have ")
print("Least percentage :")
k=input()
print("Max percentage :")
l=input()
if k.isnumeric()!= True and l.isnumeric()!= True :
  print("Insert the NUMBER of the LOWEST cloud percentage you want to search for :")
  k = input()
  print("Insert the NUMBER of the MAX cloud percentage you want to search for :")
  l = input()

print("Insert the begining date that you want to search for product (insert date as YYYYMMDD")
q=input()
print("Insert the end date that you want to search for product (insert date as YYYYMMDD")
r=input()




products=search(k,l,q,r,tiles)
print("numbers of product found "+str(len(products)))

print(*[str(k) + ':' + str(v) for k, v in products.items()], sep='\n')
decide()