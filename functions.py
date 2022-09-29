import zipfile
from zipfile import ZipFile
import os

import pyautogui
from sentinelsat import SentinelAPI


# print the main menu and get the user's option and keep it for later use
def print_menu():
    menu_options = {
        1: 'Search',
        2: 'Multi-search',
        3: 'Preprocess',
        4: 'NDVI',
        5: 'Exit' ,
    }
    for key in menu_options.keys():
        print(key, '--', menu_options[key])
    option = input('Enter your choice: ')

    while option.isnumeric() == False or  int(option)> 4 or int(option)<1 :
        option = input('Enter your choice: ')

    return int(option)


# print the multivariable search  menu and get the user's option and keep it for later use
def optionsforoption2():
    search_options = {
        1: 'Certain tile/s specific period but different cloud coverage percentage ',
        #   2: 'Multiple tiles for a specific period and cloud coverage percentage ',
        2: 'Specific tile/s in different time periods but  certain cloud coverage percentage',
        3: 'Back to main menu'

    }
    for key in search_options.keys():
        print(key, '--', search_options[key])
    option = input('Enter your choice: ')

    while   int(option)> 3 or int(option)<1 :
        option = input('Enter your choice: ')
    return int(option)

# get the number of tiles to search for and add the tiles
def tileinput():
    tilelist = []
    print('How many  Tiles do you want to search for :')

    t = input('Enter your choice: ')
    while  str(t).isnumeric() == False or int(t) < 1:
        t = input('Enter your choice: ')

    for i in range(int(t)):
        print("Add  tile")
        y = input()
        if len(y) <= 5:
            tilelist.append(str(y).upper())
        else:
            print("Wrong input please insert a tile ")


    print("The added tiles are :")
    print(tilelist)
    return tilelist
# get the cloud coverage percentage to search for in a simple search
def cloudpercentage():
    print("What cloud percentage do you the product to have ")
    print("Insert the NUMBER of the LOWEST cloud percentage you want to search for :")
    k = input('Enter your choice: ')
    while  str(k).isnumeric() == False or float(k) < 0 :
        print("Wrong input please insert a positive number")
        k = input('Enter your choice: ')
    print("Insert the NUMBER of the MAX cloud percentage you want to search for :")
    l = input('Enter your choice: ')
    while str(l).isnumeric() == False or float(l) < 0:
        print("Wrong input please insert a positive number")
        l = input('Enter your choice: ')

    return k, l;
##get the cloud coverage percentages to search for in a multisearch
def multicloudpercentage(mincloudlist, maxcloudlist):
    print("What cloud percentage do you want the product to have ")
    print("Insert the NUMBER of the LOWEST cloud percentage you want to search for :")
    k = input('Enter your choice: ')
    while str(k).isnumeric() == False or float(k) < 0:
        print("Wrong input please insert a positive number")
        k = input('Enter your choice: ')
    print("Insert the NUMBER of the MAX cloud percentage you want to search for :")
    l = input('Enter your choice: ')
    while str(l).isnumeric() == False or float(l) < 0:
        print("Wrong input please insert a positive number")
        l = input('Enter your choice: ')
    mincloudlist.append(k), maxcloudlist.append(l)
    return mincloudlist, maxcloudlist;


# get the period of time  to search for in a simple search
def dateinput():
    print("Insert the begining date that you want to search for product (insert date as YYYYMMDD)")
    q = input()
    while len(str(q).strip()) != 8:
        print(
            "Wrong input please enter again the begining date that you want to search for product (insert date as YYYYMMDD)")
        q = input()
    print("Insert the end date that you want to search for product (insert date as YYYYMMDD)")
    r = input()
    while len(str(r).strip()) != 8:
        print("Wrong input please enter againa the end date that you want to search for product (insert date as YYYYMMDD)")
        r = input()
    return q, r
# get the period of time  to search for in a multisearch
def mutlidate(liststart, listofend):
    print("What do you want the start date of the  product to be ")
    print("Insert the begining date that you want to search for product (insert date as YYYYMMDD)")
    k = input()
    print("Insert the end date that you want to search for product (insert date as YYYYMMDD)")
    l = input()
    liststart.append(k), listofend.append(l)
    return liststart, listofend;
def handlermultisearchoption1(chocie):
    tiles = tileinput()
    begindate, enddate = dateinput()
    print("how many searches do you want to do ?")

    option = input('Enter your choice: ')
    while str(option).isnumeric()==False:
        option = input('Enter your choice: ')
    nmthreads = int(option)  # store the number of threads that will be used later on
    # create list to store the cloud coverage percentages
    mincloud = list()
    maxcloud = list()
    if len(mincloud) == len(maxcloud):
        print("lists have been created and  are empty ")  # successful creation of the lists

    for i in range(int(option)):
        print("Insert values for the " + str(i + 1) + "  search")
        multicloudpercentage(mincloud, maxcloud)#fill the lists of cloud percentages
    if len(mincloud) != len(maxcloud):

        print('Internal ERROR')
#basic error handling
    return mincloud, maxcloud, begindate, enddate, tiles, nmthreads


def handlermultisearchoption2():
    tiles = tileinput()
    mincloud, maxcloud = cloudpercentage()
    print("how many searches do you want to do ?")
    option = input('Enter your choice: ')
    while str(option).isnumeric() == False:
        option = int(input('Enter your choice: '))
    nmthreads = int(option)
    begindate = list()
    enddate = list()
    if len(begindate) == len(enddate):
        print("lists have been created and  are empty ")

    for i in range(int(option)):
        print("Insert values for the " + str(i + 1) + "  search")
        mutlidate(begindate, enddate)
    if len(begindate) != len(enddate):

        print('Internal ERROR')

    return mincloud, maxcloud, begindate, enddate, tiles, nmthreads

#get the values for the variables
def option1handler():
    tiles = tileinput()
    mincloudper, maxcloudper = cloudpercentage()
    begindate, enddate = dateinput()
    return mincloudper, maxcloudper, begindate, enddate, tiles

def zipopener():
    filename = input("Paste the name of the zip file ")
    zip = zipfile.ZipFile(str(filename)).namelist()
 #   print(type(zip))
    z = zipfile.ZipFile(str(filename))
    imglist=list()
    for name in zip:
        if "IMG_DATA" in name and not name.endswith('/'):
         imglist.append(name)
         print('%s' % (name))
        else:
            continue

def readsentinelProduct(filename):
    from snappy import ProductIO
    return ProductIO.readProduct(filename)
def filecreator():
    #path = "C:/Users/PC/PycharmProjects/comballthesent/SentinelSnapIMG_DATA"
    #preprocessedpath = "C:/Users/PC/PycharmProjects/comballthesent/IMG_DATA_preprocessed"
    path = "SentinelSnapIMG_DATA"
    preprocessedpath = "/IMG_DATA_preprocessed"


    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    preprocessedexist = os.path.exists(preprocessedpath)


    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    elif not preprocessedexist:
        os.makedirs(preprocessedpath)

    filename = input("Paste the name of the zip file from the sentinel product you want to preprocess ")
    with zipfile.ZipFile(str(filename), "r") as zip_ref:
        print("file opening")
        zip_ref.extractall(path)
    filename = str(filename)
    filename = filename[:-4]

    file_path = path + "/" + filename + ".SAFE/"
    xmlpath = file_path + 'MTD_MSIL1C.xml'
    return xmlpath,filename
def removezip(zipname):
    file_path=zipname+'.zip'
    if os.path.exists(file_path):
        os.remove(file_path)
from past.builtins import raw_input
def credentialssentinel():
    user = raw_input("Username:")

    # masking the password
    # paswrd = str(maskpass.askpass(prompt="Password:", mask="#"))
    # paswrd = getpass()
    # print("Password for " + user + ":")
    paswrd = pyautogui.password(text="Password for user " + str(user) + ":",
                                title='Login to Copernicus Open Access Hub ', default='', mask='*')
    api = SentinelAPI(user, paswrd)
    return api
def ndvifileread():
    ndvimainfile = "IMG_DATA_NDVI"
    ndviexist = os.path.exists(ndvimainfile)
    if not ndviexist:
     os.makedirs(ndvimainfile)

    ndvifiletoread= input("Paste the name of the .tif preprocessedfile you want to apply ndvi ")
    subproduct='IMG_DATA_preprocessed'+'/'+ndvifiletoread
    while not os.path.exists(subproduct):
      print("File does't exists")
      ndvifiletoread = input("Paste the name of the .tif preprocessedfile you want to apply ndvi ")

    else:
     print("File exists")
     print(subproduct)
    # subproduct = 'IMG_DATA_preprocessed' + '/' + ndvifiletoread
     return subproduct
