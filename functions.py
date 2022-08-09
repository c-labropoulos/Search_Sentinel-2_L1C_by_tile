# print the main menu and get the user's option and keep it for later use
def print_menu():
    menu_options = {
        1: 'Search',
        2: 'Multi-search',
        3: 'Exit',
    }
    for key in menu_options.keys():
        print(key, '--', menu_options[key])
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')

    return option


# print the multivariable search  menu and get the user's option and keep it for later use
def optionsforoption2():
    search_options = {
        1: 'Certain tile/s specific period but different cloud coverage percentage ',
        #   2: 'Multiple tiles for a specific period and cloud coverage percentage ',
        2: 'Specific tile/s in different time periods but  certain cloud coverage percentage',
        4: 'Back to main menu'

    }
    for key in search_options.keys():
        print(key, '--', search_options[key])
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
    return option


# get the number of tiles to search for and add the tiles
def tileinput():
    tilelist = []
    print('How many  Tiles do you want to search for :')

    try:
        t = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        t = int(input('Enter your choice: '))

    for i in range(t):
        print("Add  tile")
        y = input()
        if len(y) <= 5:
            tilelist.append(str(y).upper())
        else:
            print("Wrong input try again")
            y = input()
            tilelist.append(str(y).upper())

    print("The added tiles are :")
    print(tilelist)
    return tilelist


# get the cloud coverage percentage to search for in a simple search
def cloudpercentage():
    print("What cloud percentage do you the product to have ")
    print("Insert the NUMBER of the LOWEST cloud percentage you want to search for :")

    try:
        k = float(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        k = float(input('Enter your choice: '))
    print("Insert the NUMBER of the MAX cloud percentage you want to search for :")

    try:
        l = float(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        l = float(input('Enter your choice: '))

    return k, l;


##get the cloud coverage percentages to search for in a multisearch
def multicloudpercentage(mincloudlist, maxcloudlist):
    print("What cloud percentage do you want the product to have ")
    print("Insert the NUMBER of the LOWEST cloud percentage you want to search for :")

    try:
        k = float(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        k = float(input('Enter your choice: '))
    print("Insert the NUMBER of the MAX cloud percentage you want to search for :")

    try:
        l = float(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        l = float(input('Enter your choice: '))
    mincloudlist.append(k), maxcloudlist.append(l)
    return mincloudlist, maxcloudlist;


# get the period of time  to search for in a simple search
def dateinput():
    print("Insert the begining date that you want to search for product (insert date as YYYYMMDD)")
    q = input()
    if len(q) > 8:
        print(
            "Wrong input please enter againa the begining date that you want to search for product (insert date as YYYYMMDD)")
    print("Insert the end date that you want to search for product (insert date as YYYYMMDD)")
    r = input()
    if len(r) > 8:
        print(
            "Wrong input please enter againa the end date that you want to search for product (insert date as YYYYMMDD)")
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
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        option = int(input('Enter your choice: '))
    nmthreads = option  # store the number of threads that will be used later on
    # create list to store the cloud coverage percentages
    mincloud = list()
    maxcloud = list()
    if len(mincloud) == len(maxcloud):
        print("lists have been created and  are empty ")  # successful creation of the lists

    for i in range(option):
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
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number ...')
        option = int(input('Enter your choice: '))
    nmthreads = option
    begindate = list()
    enddate = list()
    if len(begindate) == len(enddate):
        print("lists have been created and  are empty ")

    for i in range(option):
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
