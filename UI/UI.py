########################################################
##                                                    ##
##       Author:         Mohammad V.A                 ##
##       Email:          s.mohammad.alaaei@gmail.com  ##
##       First Develope: jul 21 2018                  ##
##       Version:        1.1                          ##
##                                                    ##
########################################################
from os import system, name
from UI.keyboardInput import getch

from colorama import init
from termcolor import colored

init()

class functions():
    # Clear Screen
    def clear(self): _ = system('cls') if name == 'nt' else system('clear')
    ##############

    
    def inject(self, x, num, char=' ',align='center'):
        """Print string(x) in specific location(align) and format.

        :param Any x: input String. this will be convert to String anyway.
        :param Number num: Maximum Length of output string.
        :param str char: Default prefix and suffix., defaults to ' '
        :param str align: Text alignment in output string., defaults to 'center' (options: 'left' | 'right' | 'center')

        :return str: output will be a fixed length string.

        example:
            inject('column1', 10, char=' ',align='left') => 'column1   '
            inject('column1', 10, char=' ',align='right') => '   column1'
        """

        x=str(x)
        
        #print(x,num)
        
        xx=('','')
        if x[0]=='\x1b':
            xx = (x[:5],x[-4:])
            x = x[5:-4]
            
        xLen = len(x)
        xxx= xx[0] + x + xx[1]
        if xLen>=num: return xxx
        
        comp = num-xLen
        
        if align=='center':
            comp = int(comp/2)
            x= (char*comp)+xxx+(char*comp)
            if comp==0:   x=char+x
                
        elif align=='right':
            x= (char*comp)+xxx
        else:
            x= xxx+(char*comp)
           
        return x

    def fixLength(self, x,y, plus=1, align='center',char=' '):
        """
            :param x:      (string)
            :param y:       (string)
            :param align:   (string)['left', 'right', 'center']
        """
        
        x,y=str(x),str(y)
        x1,y1 = x,y
        xx,yy = ('',''),('','')
        
        #print(x,y)
        
        # when a string started by '\x1b' means color applied to it by colored() function.
        # so, Remove extra string length from it!
        if x[0]=='\x1b':
            xx = (x[5:],x[:-4])
            x1 = x[5:-4]
        
        if y[0]=='\x1b':
            yy = (y[5:],y[:-4])
            y1 = y[5:-4]
        
        xLen = len(x1)
        yLen = len(y1)
        
        comp = xLen - yLen
        
        #print(x,y)
        if comp>=0:
            x= self.inject(x,xLen+plus,align=align,char=char)
            y= self.inject(y,xLen+plus,align=align,char=char)
        else:
            x= self.inject(x,yLen+plus,align=align,char=char)
            y= self.inject(y,yLen+plus,align=align,char=char)
        
        return x,y

class menuView():

    # def __init__(self):
    #     init()              # for colorizing terminal
    clear = functions.clear

    def showMenu(
        self,
        mnuItems,
        mnuTitle="Please Select an action:",
        selected=0,
        msg='',
        selectorBox='[{}]',
        selectorBoxColor='red',
        selectorMark='*',
        selectorMarkColor='green',
        copyright='',
        copyrightColor='white'
    ):
        """Show the menu and handle keyboard input.

            :param _type_ mnuItems: the menu items to show.
            :param int selected: index of default selected option., defaults to 0
            :param str msg: message to show at the end of menu., defaults to ''
            :param str selectorBox: selector template. {} is placeholder for selectorMark., defaults to '[{}]'
            :param str selectorBoxColor: color of the selectorBox., defaults to 'red'
            :param str selectorMark: sign or letter to mark selected item., defaults to '*'
            :param str selectorMarkColor: color of the selectorMark., defaults to 'green'
            :param str copyright: a header placeholder for banner or copyright info., defaults to ''
            :param str copyrightColor: color of the copyright., defaults to 'white'

            :return int | tuple: return selected item or code for pressing CTRL+C or Backspace. (-1: CTRL-C, -2: Backspace)
        """

        if selectorBox == '': selectorBox = '{0}'
        if selectorMark == '': selectorMark = '*'

        # TODO: changing color of selectBox. this will not work right now.
        # else:
        #     selectorBox = colored(selectorBox,selectorBoxColor if selectorBox is not '' else 'white')

        updated = True
        mnuItems[selected]['opt_selected'] = mnuItems[selected].get('opt_selected',0)
        while (1):
            if updated:
                self.clear()
                
                print(colored(copyright, copyrightColor))

                print(f"\n   %s \n" % mnuTitle)

                for i, item in enumerate(mnuItems):
                    selector = selectorBox.format(colored(selectorMark if selected == i else ' '*len(selectorMark), selectorMarkColor)) if item[
                        'selectable'] else ""

                    # Print Selector box
                    print('\t' + selector, end='', flush=True)

                    # Print Title
                    print(item['title'] if item['fgcolor'] == '' else
                          colored(item['title'], item['fgcolor']), end='', flush=True)

                    # Print Options
                    print('' if len(item['options']) == 0 or type(item['options']) != tuple else
                          colored("\t< ",'green')+
                          colored(item['options'][item['opt_selected']],'yellow' if item['opt_fgcolor'] == '' else item['opt_fgcolor'])+
                          colored(" >",'green')
                          )

                print(colored('\n   Press CTRL+C to exit', 'yellow'))
                print(colored('   ' + msg, 'yellow'))

                updated = False

            key = getch()
            if key == '\r':
                return selected, mnuItems[selected]['opt_selected']
            elif key == 'CTRL+C':
                return -1
            elif key == 'BACKSPACE':
                return -2

            elif key == 'UP':
                oldSelected = selected
                while (1):
                    if selected > 0:
                        selected -= 1
                        # updated = True
                    else:
                        selected = oldSelected
                        break

                    if mnuItems[selected]['selectable']:
                        updated = True
                        break

            elif key == 'DOWN':
                oldSelected = selected
                while (1):
                    if selected < len(mnuItems) - 1:
                        selected += 1
                        # updated = True
                    else:
                        selected = oldSelected
                        break

                    if mnuItems[selected]['selectable']:
                        updated = True
                        break

            elif key == 'RIGHT':
                if len(mnuItems[selected]['options']) >0 and mnuItems[selected]['opt_selected'] < len(mnuItems[selected]['options'])-1:
                    mnuItems[selected]['opt_selected'] += 1
                    updated = True

            elif key == 'LEFT':
                if len(mnuItems[selected]['options']) >0 and mnuItems[selected]['opt_selected'] >0:
                    mnuItems[selected]['opt_selected'] -= 1
                    updated = True


    def createMenu(
        self,
        mnuItems,
        mnuTitle="Please Select an action:",
        selected=0,
        msg='',
        selectorBox='[{}]',
        selectorBoxColor='white',
        selectorMark='*',
        selectorMarkColor='green',
        copyright='',
        copyrightColor='white'
    ):
        """
            ### All arguments are optional
            mnuItems = [
                         {
                          'title' : 'menu title',
                          'fgcolor': 'forground color',
                          'options': (tuple) ('item options',...),
                          'opt_selected': (int) default selected option number,
                          'opt_fgcolor': 'options forground color',
                          'selectable': (boolean) [default=True | False],
                          'action': funtion_to_run,
                          'action_kwargs': {
                                              'arg1': 'value',
                                              ...
                                           }
                         }
                         {...}
                       ]
        """

        titles = []
        for i, item in enumerate(mnuItems):
            # Set default values
            item['action'] = item.get('action', None)
            item['action_kwargs'] = item.get('action_kwargs', {})

            titles.append({
                'title': item.get('title', ''),
                'fgcolor': item.get('fgcolor', ''),
                'options': item.get('options', ()),
                'opt_fgcolor': item.get('opt_fgcolor', ''),
                'opt_selected': item.get('opt_selected', 0),
                'selectable': item.get('selectable', True),
            })

        while (1):

            selected = self.showMenu(
                titles,
                mnuTitle=mnuTitle,
                selected=selected,
                msg=msg,
                selectorBox=selectorBox,
                selectorBoxColor=selectorBoxColor,
                selectorMark=selectorMark,
                selectorMarkColor=selectorMarkColor,
                copyright=copyright,
                copyrightColor=copyrightColor
                )
            
            if type(selected)==tuple:
                selected,Optselected = selected
            else:
                Optselected = 0
            
            self.clear()
            
            if selected == -1:
                return -1
            elif selected == -2:
                # print(selected)
                return -2
            else:
                if mnuItems[selected]['action'] == None:
                   return selected, Optselected
                else:
                    sub = mnuItems[selected]['action'](**mnuItems[selected]['action_kwargs'])
                    if sub!= None:
                        if sub <0: return sub
            

            if mnuItems[selected]['action'] not in (None, self.createMenu):
                getch(colored("\nPress any key to continue", 'cyan'))

class listView():
    string = functions()

    def PrintHeader(self, lst,color='yellow',minLength=10, msg='',msgColor='green',align='left'):
        length = 0
        res=''
        for header in lst:
            if minLength> len(str(lst[header])):
                str2 = 'x' * minLength
            else:
                str2 = str(lst[header])
                
            #print(str2,len(str2))
            header = self.string.fixLength(str(header),str2,align=align)[0]
            #print(str(header),tmp2,len(str(header)),len(tmp2))
            
            length+=len(header)
            
            res +=colored(header,color)
        
        if msg!='':
            print()
            print(colored((' ' *(int(length/2)-int(len(msg)/2))) + msg,msgColor))
            
        print(res)
        print("="*length)

    def Print(self, lst,headerColor = 'yellow',minLength=10, align='left'):
        # cities={
        #     'لاهیجان':   'Lahijan',
        #     'رودسر':    'Roudsar',
        #     'سیاهکل':   'Siahkal'
        # }
        
        
        if len(lst)>0:
            #print(lst)
            for index,item in enumerate(lst):
                #print(index, item)

                # if lst[index].get('city',False):
                #     lst[index]['city'] = cities.get(lst[index]['city'],lst[index]['city'])     #change persian to english
                
                if index%40==0: 
                    if index!=0:
                        print(colored('\n'+ self.string.fixLength('[press ENTER to continue]','x'*minLength)[0],'magenta'))
                        key=''
                        while(key!='\r'):
                            key=getch()
                    self.PrintHeader(item, color=headerColor,minLength=minLength,align=align)
                
                for i in item:
                    #print(i,item)
                    if minLength> len(str(i)):
                        str2 = 'x' * minLength
                    else:
                        str2 = str(i)
                        
                    #print(item[i],str2)
                    temp1 = self.string.fixLength(item[i] if item[i]!='' else 'None',str2,align=align)[0]
                    print(colored(temp1,"yellow" if index%2==0 else "white"),end="",flush=True)
                    
                print()
            print()
        else:
            print(colored('Nothing to show!','yellow'))

class loadingBar():
    def __init__(self, maxValue , barLength=50, fillChar="=", emptyChar=" ", fillColor='white', emptyColor='white', showPercent=False, style="{}[{}{}] {}  "):
        self.__maxValue = maxValue
        self.__barLength = barLength
        self.__fillColor = fillColor
        self.__emptyColor = emptyColor
        self.__showPercent = showPercent
        self.__fillChar = fillChar
        self.__emptyChar = emptyChar
        self.__style = style

        self.__valuePerPercent = maxValue/barLength

        # print(maxValue, self.__valuePerPercent)

    def show(self, value, label=''):
        filledCount = float("{0:.2f}".format(((value+1) * self.__barLength)/self.__maxValue))
        emptyCount = int(self.__barLength - filledCount)

        if self.__showPercent:
            percent = '{0:.2f}%'.format(((value+1)/self.__maxValue)*100) # calculate filled percent and output in float format like: 0.00
            percent = functions.inject(self, percent, 9, align='center') # use inject() to prevent juddering. this will give us a 7 character length text (7 is based on max length of output percent)
        else:
            percent = ''
        
        return self.__style.format( label,
                                    colored(self.__fillChar * int(filledCount),self.__fillColor),
                                    colored(self.__emptyChar * emptyCount,self.__emptyColor),
                                    colored(percent,self.__fillColor)
                                )
        # return (currPercent, emptyPercent, self.__maxValue, value)

