from sys import exit
from termcolor import colored
from UI.keyboardInput import getch
from UI.UI import *
from time import sleep

menu = menuView()       # to create menu
funcs = functions()     # some string functions
List = listView()       # to show tables

# make a copyright header
info = {
    'version':        "1.1",
    'author':         "Mohammad V.A",
    'email':          "s.mohammad.alaaei@gmail.com",
    'modified_date':  "may 7 2024",
    'create_date':    "jul 21 2018",
}

copyright  = ("#"*57)+"\n##"+(" "*53)+"##\n##       Author:         {}##\n##       Email:          {}##\n"
copyright += "##       First Develope: {}##\n##       Last Modified:  {}##\n##       Version:        {}##\n##"+(" "*53)+"##\n"+("#"*57)
copyright = copyright.format(
                                funcs.inject(info['author'], 30,align='left'),
                                funcs.inject(info['email'], 30,align='left'),
                                funcs.inject(info['create_date'], 30,align='left'),
                                funcs.inject(info['modified_date'], 30,align='left'),
                                funcs.inject(info['version'], 30,align='left')
                            )



# Some test functions, feel free to edit them
def function_1():
    print(f'just a regular function with no input.\nnote that you should not use any %s in functions.' % colored('return()','yellow'))

def function_2(group):
    print(f'input paramer: %s' % group)

def subMenu():
    mnuItems = [
                {
                    'title':    ' - Who are you?'
                },
                {
                    'title':    ' - hello to',
                    'options':  ('world','earth','universe',),
                    # no Action needed. we handle it in next lines
                }
            ]
                    
    selected = menu.createMenu(mnuItems, msg='press Backspace to go back')
    #getch(str(selected))

    if type(selected)==tuple:
        selected_item,selected_option = selected
    else:
        if selected<0: return selected # basically pass codes like Exit or Back to parent
        selected_item = selected

    if selected_item == 0:
        fname = input("Your first name:")
        lname = input("Your last name:")

        barMaxLength = 50

        # create loading bar instance
        bar = loadingBar(
            maxValue=barMaxLength,
            barLength=50,
            fillChar='█',
            fillColor='green',
            emptyChar='█',
            emptyColor='white',
            style="{0} {2}{1}{3}{1}{2}", # feel free to test other styles like: {0} {1}{2} {3} or even this for right to left fill: {3} {2}{1} {0}
            showPercent=True
            )
        
        # Simulate loading
        for i in range(barMaxLength):
            print(bar.show(i,colored('Loading...','cyan')),end='\r',flush=True)   # print Loading bar
            sleep(0.05)

        # funcs.clear()
        print(f"\nNice to meet you %s %s" % (fname,lname))

    elif selected_item==1:
        if selected_option==0:
            print("Hello World!")
        elif selected_option==1:
            print("Hello Earth!!")
        elif selected_option==2:
            print("Hello Universe!!!")

def printTable():
    testDate = []
    for i in range(70):
        testDate.append({'Row ID':i, 'Column 1': 'test data', 'Column 2': i*2, 'Test': True if i%2==0 else False})

    List.Print(testDate, align='center')

def back():
    return -2

mainMenuOptions = ('Iran','Canada','United States','United Kingdoms')
def mainMenuOption(selectedIndex, selectedOption):
    getch((f"selected Column: %i\nyou selected [%s] as country" % (selectedIndex,mainMenuOptions[selectedOption])) + colored("\n\nPress any key to continue", 'yellow'))


# Main function
def main():
    # Some sub-menu items
    updateItems = [
        {
            'title': ' - First item',
            'action': function_1,
            'action_kwargs': {}
        },
        {
            'title': ' - Function with parameter',
            'action': function_2,
            'action_kwargs': {
                'group': '1',
            }
        },
        {'selectable': False},  # Make some space
        {
            'title': ' - not selectable',
            'selectable': False
        },
        {'selectable': False},  # Make some space
        {
            'title': ' <-Main',
            'action': back,
            'fgcolor': 'yellow'
        },
        {
            'title': ' - Exit',
            'fgcolor': 'red',
            'action': exit,
        },
    ]
    nestedMenu = [
        {
            'title': ' Just another menu!',
            'selectable': False
        },
        {
            'title': ' lambda item',
            'action': lambda: print('selected Item 1')
        },
        {
            'title': ' show table',
            'action': printTable
        },
        {
            'title': ' Check this !',
            'action': subMenu,
            'fgcolor': 'magenta',
        },
        {'selectable': False},  # Make some space
        {
            'title': ' Main',
            'action': back,
            'fgcolor': 'yellow'
        },
        {
            'title': ' Exit',
            'fgcolor': 'red',
            'action': exit,
        },
    ]
    viewItems = [
        {
            'title': ' - Nested Menu ->',
            'action': menu.createMenu,
            'action_kwargs': {
                'mnuItems': nestedMenu,
                'msg': 'press ' + colored('Backspace','blue') + colored(' to go back','yellow'),
                'selectorBox': '',
                'selectorMark': '->',
                'selectorMarkColor': 'red',
                'selected': 1,       # when your first item is not selectable, you need to define first selected item. otherwise will get errors.
                'copyright': copyright
            }
        },
        {'selectable': False},  # Make some space
        {
            'title': ' - Exit',
            'fgcolor': 'red',
            'action': exit,
        },
    ]


    # This is actual Main Menu that you call for first time.
    mainItems = [
        {
            'title': ' - goto next menu >',
            'fgcolor': 'white',
            'action': menu.createMenu,
            'action_kwargs': {
                'mnuItems': updateItems,
                'msg': 'press Backspace to go back',
                'selectorMarkColor': 'green',
            }
        },
        {
            'title': ' - Another Menu >',
            'fgcolor': 'white',
            'action': menu.createMenu,
            'action_kwargs': {
                'mnuItems': viewItems,
                'mnuTitle': 'You can even change the menu Title !\n   Select an Item to explore:',
                'msg': 'press Backspace to go back',
                'selectorMark': '♥',
                'selectorMarkColor': 'green',
            }
        },
        {
            'title': ' - select country',
            'fgcolor': 'blue',
            'options':  mainMenuOptions,
        },
        {'selectable': False},  # Make some space
        {
            'title': ' - Exit',
            'fgcolor': 'red',
            'action': exit,
            'action_kwargs': {}
        },
    ]

    mainSelected = 0

    while (1):

        mainSelected = menu.createMenu(mainItems,copyright=copyright)

        funcs.clear()

        if mainSelected == -2:  # on Backspace
            mainSelected = 0
            continue
            
        elif mainSelected == -1:
            break  # Exit
        elif type(mainSelected) == tuple:   # this is for handling 'select country' item in main menu
            mainMenuOption(mainSelected[0], mainSelected[1])

        else:
            # this is required to give you some time to read output data
            getch(str(mainSelected)+colored("\nPress any key to continue", 'yellow'))


# Start Main function:
if __name__ == "__main__": main()
