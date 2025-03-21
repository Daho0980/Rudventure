import time

from .                  import anchor
from Game.utils.modules import Textbox

class Graphs:
    @staticmethod
    def IOAD(length:int) -> list[int]:
        """
        ### In&Out Animation Division function.
        """
        output      = []
        halfLength  = round(length/2)
        bifurcation = 0

        if length%2:
            length -= 1
            output.append(1)

        for i in range(1, length):
            if (sum(output)-1+i) > halfLength:
                bifurcation = i-1

                break

            output.append(i)
        bifurcation = bifurcation or halfLength

        output += [i for i in range(bifurcation, 0, -1)]

        remainingValue = length-sum(output)
        remainingValue = [round(remainingValue/2), int(remainingValue/2)]

        return [1]*remainingValue[1]+output+[1]*remainingValue[0]

    @staticmethod
    def OOAD(length:int) -> list[int]:
        """
        ### Only Out Animation Division function.
        """
        output = []
        
        for i in range(1, length):
            if sum(output)+i > length:
                remainingValue = length-sum(output)
                break
            output.append(i)

        output += [remainingValue]

        return output[::-1]

    @staticmethod
    def SOAD(length:int) -> list[int]:
        """
        ### Super Out Animation Division function.
        """
        output = []

        while True:
            if length == 1: output.append(1); break

            if length%2: output.append(int(length/2)+1)
            else       : output.append(int(length/2))
            length = int(length/2)

        return output

class Box:
    @staticmethod
    def forward(stdscr                        ,
                row          :int             ,
                column       :int             , 
                lineType     :str             ,
                boxColor     :str      =""    ,
                animationType:str      ='OOAD',
                frameDelay   :float|int=0.018 ,
                connectDelay :float|int=0      ) -> str:
        """
        This animation can only work when the game is static.
        ex) In mainMenu, whatever before playing the game
        """
        animation = {
            'IOAD' : Graphs.IOAD,
            'OOAD' : Graphs.OOAD,
            'SOAD' : Graphs.SOAD
        }[animationType]

        r = animation(row)
        c = animation(column)

        totalC = 0
        for cc in c:
            totalC += cc

            stdscr.erase()
            anchor(
                stdscr,
                Textbox.TextBox(
                    ''.join([" "*(totalC)]),
                    AMLS           =True,
                    LineType       =lineType,
                    coverColor     =boxColor,
                    alwaysReturnBox=False
                ),
                addOnyx=[1, 0]
            )
            stdscr.refresh()
            time.sleep(frameDelay)
        
        time.sleep(connectDelay)

        totalR = 0
        for rc in r:
            totalR += rc

            stdscr.erase()
            anchor(
                stdscr,
                Textbox.TextBox(
                    '\n'.join([" "*column]*totalR),
                    AMLS           =True,
                    LineType       =lineType,
                    coverColor     =boxColor,
                    alwaysReturnBox=False
                ),
                addOnyx=[1, 0]
            )
            stdscr.refresh()
            time.sleep(frameDelay)

        return Textbox.TextBox(((" "*column)+"\n")*row, AMLS=True, LineType=lineType)
    
    @staticmethod
    def reverse(stdscr                        ,
                row          :int             ,
                column       :int             , 
                lineType     :str             ,
                boxColor     :str      =""    ,
                animationType:str      ='OOAD',
                frameDelay   :float|int=0.018 ,
                connectDelay :float|int=0      ) -> str:
        animation = {
            'IOAD' : Graphs.IOAD,
            'OOAD' : Graphs.OOAD,
            'SOAD' : Graphs.SOAD
        }[animationType]

        r = animation(row)
        c = animation(column)


        for i, n in enumerate(r):
            stdscr.erase()

            anchor(
                stdscr,
                Textbox.TextBox(
                    '\n'.join([" "*column]*(n+sum(r[i+1:]))),
                    AMLS           =True,
                    LineType       =lineType,
                    coverColor     =boxColor,
                    alwaysReturnBox=False
                ),
                addOnyx=[1, 0]
            )
            stdscr.refresh()

            time.sleep(frameDelay)

        time.sleep(connectDelay)

        for i, n in enumerate(c):
            stdscr.erase()
            anchor(
                stdscr,
                Textbox.TextBox(
                    ''.join([" "*(n+sum(c[i+1:]))]),
                    AMLS           =True,
                    LineType       =lineType,
                    coverColor     =boxColor,
                    alwaysReturnBox=False
                ),
                addOnyx=[1, 0]
            )
            stdscr.refresh()
            
            time.sleep(frameDelay)

        stdscr.erase()
        stdscr.refresh()

        return Textbox.TextBox(((" "*column)+"\n")*row, AMLS=True, LineType=lineType)
