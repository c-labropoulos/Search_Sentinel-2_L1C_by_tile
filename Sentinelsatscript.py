from collections import OrderedDict
import subprocess
from matplotlib import pyplot as plt, cm

from functions import print_menu, tileinput, cloudpercentage, dateinput, optionsforoption2, multicloudpercentage, \
    handlermultisearchoption1, handlermultisearchoption2, option1handler, zipopener, credentialssentinel, removezip, \
    ndvifileread
import pyautogui as pyautogui
from past.builtins import raw_input
from sentinelsat import SentinelAPI
from threading import Thread
import queue
import logging
import urllib3
import maskpass  # importing maskpass library
import  numpy as np
from zipfile import ZipFile

from preprocessfunctions import readxml, resampleandsubset, showsub, savefile, ndviproduct

logging.basicConfig(format='%(message)s', level='INFO')

my_queue = queue.Queue()
#function to get products dictionary from each thread later on
def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

def search(x,y,z,t,tiles):
    #x : minimum percentage of cloud coverage
    #y: maximum percentage of cloud coverage
    #z : beginning date to search for the product
    #t : end date to search for the product
    #tiles : the tiles on the "world map" that we are going to search
    query_kwargs = {
        'cloudcoverpercentage': (float(x), float(y)),

        'platformname': 'Sentinel-2',#satelite that we are using
        'producttype': 'S2MSI1C',#the data products we are focusing on
        'date': (str(z), str(t))}

    products = dict()
    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)
    return products#returns a dictionary with the products and their details that were found based on the previous criteria
@storeInQueue#store the return dict of the function in the queue so we can use it outside of the thread
def multisearch(x,y,z,t,tiles):
    # x : minimum percentage of cloud coverage
    # y: maximum percentage of cloud coverage
    # z : beginning date to search for the product
    # t : end date to search for the product
    # tiles : the tiles on the "world map" that we are going to search
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
    return  products#returns a dictionary with the products and their details that were found based on the previous criteria
#a function for the user to decide if the user wants to download all the products or a specific amount of them
def decide():
    print("Do you want to download all the products \t Y/N")
    dicision = input()
    if dicision == 'y' or dicision == 'Y':
        api.download_all(products)#download all the products
    elif dicision == 'n' or dicision == 'N':
        print("Do you want to download one or only a specific amount of products\t Y/N")
        decision = input()
        if decision == 'y' or decision == 'Y':
            print("How many products do you want to download")
            prnum = input()
            if prnum.isnumeric() != True  :
                print("Insert the NUMBER of products you want to download")
                prnum = input()
            for i in range(int(prnum)):
                print("Please provide the code of the product \nEXAMPLE OF CODE : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx ")
                code = str(input())
                product_info = api.get_product_odata(code)
                is_online = product_info['Online']
                if is_online:
                    print(f'Product {code} is online. Starting download.')
                    api.download(code)
                else:
                    print(f'Product {code} is not online.')
                    api.trigger_offline_retrieval( code)
                #api.download(code)#download the product with a specific code
        elif decision == 'n' or decision == 'N':
            print("Printing the products ....")
            print(*[str(k) + ':' + str(v) for k, v in products.items()], sep='\n')
            exit()
        else:
            print("WRONG INPUT,BE CAREFULL")
            decide()
    else:
        print("ERROR : WRONG INPUT\n")
        decide()
def multisearchdecide(dict):#a function for the user to decide if the user wants a specific amount of the products after a search with non standard variables
    print("Do you want to download any of the products \t Y/N")
    dicision = input()
    if dicision == 'n' or dicision == 'N':
        print("These are the products")
        print(*[str(k) + ':' + str(v) for k, v in dict.items()], sep='\n')
        print("Going back to the main menu")
        subprocess.call(['python', 'Sentinelsatscript.py'])
    elif dicision == 'y' or dicision == 'Y':

            print("How many products do you want to download")
            prnum = input()
            i = 1
            if prnum.isnumeric() != True:
                print("Insert the NUMBER of products you want to download")
                prnum = input()
            for i in range(int(prnum)):

                print("Please provide the code of the product \nEXAMPLE OF CODE : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx ")
                code = str(input())
                is_online = api.is_online( code)


                if is_online:
                    print(f'Product {code} is online. Starting download.')
                    api.download( code)
                else:
                    print(f'Product {code} is not online.')
                    api.trigger_offline_retrieval( code)
                while i>1:
                    print(
                        "Please provide another  code of a product you want to downlaod \nEXAMPLE OF CODE : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx ")
                    code = str(input())
                    is_online = api.is_online(code)
               # api.download(code)#download the product with a specific code
    else:
        print("ERROR : WRONG INPUT\n")
        multisearchdecide()
option=print_menu()
#go to functions.py to see more details about the print_menu()
#https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59 find tiles from the map in the site
#34SEJ
#33VUC, 33UUB


if option == 1:
    api=credentialssentinel()
    text = "Find some useful testing tiles here"
    target = "https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59"
    print(f"\n\u001b{target}\u001b\\{text}\u001b\u001b\\")
    mincloudper, maxcloudper, begindate, enddate, tiles= option1handler()#function to get the content of the variables which based on the search will be conducted
    products=search(mincloudper, maxcloudper, begindate, enddate,tiles)#search and store in dict the producst that fulfill the search filters
    print(*['product code '+str(k) + '\t product details : ' + str(v) for k, v in products.items()], sep='\n')
    decide()

elif option == 2:
    api = credentialssentinel()
    text = "Find some useful testing tiles here"
    target = "https://eatlas.org.au/data/uuid/f7468d15-12be-4e3f-a246-b2882a324f59"
    print(f"\n\u001b{target}\u001b\\{text}\u001b\u001b\\\n")
    option=optionsforoption2()#go to functions.py to see more details about the optionsforoption2()

    if option == 1:
        mincp,maxcp,begindate,enddate,tiles,t=handlermultisearchoption1(option)#function to fill all the variables for this option
        tlist=[]#an empty list that will be later used to store the threads used
        prodict=dict()# a dictionary  that we will store the products dictionaries

        for i in range(t):
            t = Thread(target=multisearch,args=(mincp[i],maxcp[i],begindate,enddate,tiles))
            tlist.append(t)# store the new thread in a list of threads
            t.start()# start a new thread
            #start a thread that will run  the function multisearch with a specific set of variables
            my_data = my_queue.get()#create a queue object that will store the return values(product's dictionary) of the multisearch function
            prodict[i]=my_data#store the dictionary returned from the multisearch function from the thread in the prodict dictionary cretaing a nested dictionary

        for t in tlist:
          t.join()#finish thread

        for i in range(len(prodict)):
            multisearchdecide(prodict[i])
            #run the multisearchdecide function based on each dictionary of producst stored in the nested dictionary
       # print_menu()
    elif option == 2:
        mincp, maxcp, begindate, enddate, tiles, t=handlermultisearchoption2()##function to fill all the variables for this option
        tlist = []#an empty list that will be later used to store the threads used
        prodict = dict()
        for i in range(t):
            t = Thread(target=multisearch, args=(mincp, maxcp, begindate[i], enddate[i], tiles))
            tlist.append(t)# store the new thread in a list of threads
            t.start()# start a new thread
            # start a thread that will run  the function multisearch with a specific set of variables
            my_data = my_queue.get()#create a queue object that will store the return values(product's dictionary) of the multisearch function
            prodict[i] = my_data#store the dictionary returned from the multisearch function from the thread in the prodict dictionary cretaing a nested dictionary

        for t in tlist:
            t.join()#finish thread
        for i in range(len(prodict)):
            multisearchdecide(prodict[i])
    # run the multisearchdecide function based on each dictionary of producst stored in the nested dictionary

    elif option == 3:
        print('Redirecting back to main menu')
        subprocess.call(['python', 'Sentinelsatscript.py'])
    else:
        print('Invalid option. Please enter a number between 1 and 3.')
elif option == 3:
    xmlpath,zipname,product=readxml()
    sub_product=resampleandsubset(product)
    savefile(sub_product,zipname)
    answer = input("Do yo to see the the preprocessed product Y/N : ")
    while answer.lower().strip() not in ('y', 'n'):
        answer = input("Do yo to see the the preprocessed product Y/N : ")

    if answer.lower().strip() == 'n':
        print("Going back to main menu")
        subprocess.call(['python', 'Sentinelsatscript.py'])
    elif answer.lower().strip() == 'y':
        sub_b6 = sub_product.getBand('B6')
        print("band read")
        width = sub_b6.getRasterWidth()
        height = sub_b6.getRasterHeight()
        print("subset size : ", width, height)
        sub_b6_data = np.zeros(width * height, dtype=np.float32)
        sub_b6.readPixels(0, 0, width, height, sub_b6_data)
        sub_b6_data.shape = height, width

        plt.figure(1)
        fig = plt.imshow(sub_b6_data, cmap=cm.gray)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.show()
        print("Going back to main menu")
        subprocess.call(['python', 'Sentinelsatscript.py'])
elif option == 4:
    product=ndvifileread()
    ndviproduct(product)

else :
   print('Exiting')
   exit()
