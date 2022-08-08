from collections import OrderedDict
import colored as colored
from functions import print_menu, tileinput, cloudpercentage, dateinput, optionsforoption2, multicloudpercentage, \
    handlermultisearchoption1
import pyautogui as pyautogui
from past.builtins import raw_input
from sentinelsat import SentinelAPI
import getpass
from time import sleep, perf_counter
from threading import Thread

print("Insert Credentials for Copernicus Open Access Hub ")
user = raw_input("Username:")
#print("Password for " + user + ":")
paswrd = pyautogui.password(text="Password for user " + str(user) + ":", title='Login to Copernicus Open Access Hub ', default='', mask='*')
api = SentinelAPI(user, paswrd)

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
    print("\n Numbers of product found " + str(len(products))+ " in the period between "+str(z)+" and "+str(t)+" with cloud coverage percentage between "+str(x)+" and "+str(y) )
   # print("for search variables :cloudcoverpercentage"+str(x)+"\t"+str(y)+"date"+str(z)+"\t"+str(t))
    print(*['product code '+str(k) + '\t product details : ' + str(v) for k, v in products.items()], sep='\n')
    print("\n")
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
        print("ERROR : WRONG INPUT\nGoing back to the menu")
        print_menu()
print_menu()

#https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59 find tiles from the map in the site
#34SEJ
text = "Find some useful testing tiles here"
target = "https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59"
print(f"\u001b{target}\u001b\\{text}\u001b\u001b\\")
try:
            option = int(input('Enter your choice: '))
except:
            print('Wrong input. Please enter a number ...')

        #Check what choice was entered and act accordingly
if option == 1:
    tiles = tileinput()
    mincloudper, maxcloudper = cloudpercentage()
    begindate, enddate = dateinput()

    products=search(mincloudper, maxcloudper, begindate, enddate,tiles)
    print("numbers of product found " + str(len(products)))
    print(*[str(k) + ':' + str(v) for k, v in products.items()], sep='\n')
    decide()
elif option == 2:
    optionsforoption2()
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
    if option == 1:
        mincp,maxcp,begindate,enddate,tiles,t=handlermultisearchoption1(option)
        tlist=[]
        for i in range(t):
            t = Thread(target=multisearch(mincp[i],maxcp[i],begindate,enddate,tiles))
            tlist.append(t)
            t.start()
        for t in tlist:
            t.join()





        #mincloudper1, maxcloudper1 = cloudpercentage()
       # print("Insert values for the first  search")
        #mincloudper2, maxcloudper2 = cloudpercentage()

    elif option == 2:
        print('Handle option \'Option 2\'')
    elif option == 3:
        print('Handle option \'Option 3\'')
    elif option == 4:
        print('Redirecting back to main menu')
        print_menu()
    else:
        print('Invalid option. Please enter a number between 1 and 4.')
elif option == 4:
            print('Thanks message before exiting')
            exit()
else:
            print('Invalid option. Please enter a number between 1 and 4.')



