from collections import OrderedDict
import colored as colored
from functions import print_menu, tileinput, cloudpercentage, dateinput, optionsforoption2, multicloudpercentage, \
    handlermultisearchoption1, handlermultisearchoption2, option1handler
import pyautogui as pyautogui
from past.builtins import raw_input
from sentinelsat import SentinelAPI
import getpass
from time import sleep, perf_counter
from threading import Thread
import queue
print("Insert Credentials for Copernicus Open Access Hub ")
user = raw_input("Username:")
#print("Password for " + user + ":")
paswrd = pyautogui.password(text="Password for user " + str(user) + ":", title='Login to Copernicus Open Access Hub ', default='', mask='*')
api = SentinelAPI(user, paswrd)

my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

def search(x,y,z,t,tiles):
    query_kwargs = {
        'cloudcoverpercentage': (float(x), float(y)),
        # "cloudcoverpercentage":'5',
        'platformname': 'Sentinel-2',
        'producttype': 'S2MSI1C',
        'date': (str(z), str(t))}

    products = dict()
    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)
    return products

@storeInQueue
def multisearch(x,y,z,t,tiles):
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
    print("\nNumbers of product found " + str(len(products))+ " in the period between "+str(z)+" and "+str(t)+" with cloud coverage percentage between "+str(x)+" and "+str(y) )

    print(*['product code '+str(k) + '\t product details : ' + str(v) for k, v in products.items()], sep='\n')
    print("\n")
    return  products
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
            print("Printing the products ....")
            print(*[str(k) + ':' + str(v) for k, v in products.items()], sep='\n')
            exit()
    else:
        print("ERROR : WRONG INPUT\nGoing back to the menu")
        print_menu()
def multisearchdecide(dict):
    print("Do you want to download any of the products \t Y/N")
    dicision = input()
    if dicision == 'n' or dicision == 'N':
        print("These are the products")
        print(*[str(k) + ':' + str(v) for k, v in dict.items()], sep='\n')
        print("Going back to the main menu")
        print_menu()
    elif dicision == 'y' or dicision == 'Y':

            print("How many products do you want to download")
            prnum = input()
            if prnum.isnumeric() != True:
                print("Insert the NUMBER of products you want to download")
                prnum = input()
            for i in range(int(prnum)):
                print("Please provide the code of the product \nEXAMPLE OF CODE : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx ")
                code = str(input())
                api.download(code)
    else:
        print("ERROR : WRONG INPUT\nGoing back to previous menu")
        optionsforoption2()
option=print_menu()

#https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59 find tiles from the map in the site
#34SEJ
#33VUC, 33UUB


if option == 1:
    text = "Find some useful testing tiles here"
    target = "https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59"
    print(f"\n\u001b{target}\u001b\\{text}\u001b\u001b\\")
    mincloudper, maxcloudper, begindate, enddate, tiles= option1handler()
    products=search(mincloudper, maxcloudper, begindate, enddate,tiles)
    print(*['product code '+str(k) + '\t product details : ' + str(v) for k, v in products.items()], sep='\n')
    decide()
elif option == 2:
    text = "Find some useful testing tiles here"
    target = "https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59"
    print(f"\n\u001b{target}\u001b\\{text}\u001b\u001b\\\n")
    option=optionsforoption2()

    if option == 1:
        mincp,maxcp,begindate,enddate,tiles,t=handlermultisearchoption1(option)
        tlist=[]
        prodict=dict()

        for i in range(t):
            t = Thread(target=multisearch,args=(mincp[i],maxcp[i],begindate,enddate,tiles))
            tlist.append(t)
            t.start()
            my_data = my_queue.get()
            prodict[i]=my_data

        for t in tlist:
          t.join()

        for i in range(len(prodict)):
            multisearchdecide(prodict[i])
    elif option == 2:
        mincp, maxcp, begindate, enddate, tiles, t=handlermultisearchoption2()
        tlist = []
        prodict = dict()
        for i in range(t):
            t = Thread(target=multisearch, args=(mincp, maxcp, begindate[i], enddate[i], tiles))
            tlist.append(t)
            t.start()
            my_data = my_queue.get()
            prodict[i] = my_data
        for t in tlist:
            t.join()
        for i in range(len(prodict)):
            multisearchdecide(prodict[i])


    elif option == 3:
        print('Redirecting back to main menu')
        print_menu()
    else:
        print('Invalid option. Please enter a number between 1 and 3.')
elif option == 3:
            print('Exiting')
            exit()
else:
            print('Invalid option. Please enter a number between 1 and 4.')
            option = int(input('Enter your choice: '))


