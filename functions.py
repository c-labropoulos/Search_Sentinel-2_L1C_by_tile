def print_menu():
    menu_options = {
        1: 'Search',
        2: 'Multi-search',
        3: 'Option 3',
        4: 'Exit',
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
def optionsforoption2():
    search_options = {
        1: 'Certain tile/s specific period but different cloud coverage percentage ',
        2: 'Multiple tiles for a specific period and cloud coverage percentage ',
        3: 'Specific tile/s in different time periods but  certain cloud coverage percentage',
        4: 'Back to main menu'

    }
    for key in search_options.keys():
        print(key, '--', search_options[key])
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
        tilelist.append(str(y).upper())

    print("The added tiles are :")
    print(tilelist)
    return tilelist
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

    return  k,l;


def multicloudpercentage(mincloudlist,maxcloudlist):
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
    mincloudlist.append(k),maxcloudlist.append(l)
    return mincloudlist, maxcloudlist;
def dateinput():
    print("Insert the begining date that you want to search for product (insert date as YYYYMMDD")
    q = input()
    print("Insert the end date that you want to search for product (insert date as YYYYMMDD")
    r = input()
    return q,r
def handlermultisearchoption1(chocie):


        tiles = tileinput()
        begindate, enddate = dateinput()
        print("how many searches do you want to do ?")
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
            option = int(input('Enter your choice: '))
        nmthreads=option
        mincloud = list()
        maxcloud = list()
        if len(mincloud) == len(maxcloud):
            print("lists have been created and  are empty ")

        for i in range(option):
            print("Insert values for the " + str(i + 1) + "  search")
            multicloudpercentage(mincloud, maxcloud)
        if len(mincloud) != len(maxcloud):
            # text =
            # colored_text = colored(255, 0, 0, text)
              print('Internal ERROR')
           # for i in range(len(maxcloud)):
              #  print(str(mincloud[i]) + "\t" + str(maxcloud[i]))
        return  mincloud,maxcloud,begindate,enddate,tiles,nmthreads
#def multiserachhandler():

