import time

from Game.utils.modules  import Textbox
from Game.utils.graphics import addstrMiddle

class graphs:
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
            if sum(output)-1+i > halfLength:
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
            else:        output.append(int(length/2))
            length = int(length/2)

        return output
    
class box:
    @staticmethod
    def forward(
            stdscr,
            row:int,
            column:int, 
            lineType:str,
            boxColor:str          ="",
            animationType:str     ='OOAD',
            frameDelay:float|int  =0.018,
            connectDelay:float|int=0
            ) -> str:
        """
        This animation can only work when the game is static.
        ex) In mainMenu, Whatever before playing the game
        """

        animation = {
            'IOAD' : graphs.IOAD,
            'OOAD' : graphs.OOAD,
            'SOAD' : graphs.SOAD
        }[animationType]

        r = animation(row)
        c = animation(column)

        for i, n in enumerate(c):
            stdscr.erase()
            addstrMiddle(
                stdscr,
                Textbox.TextBox(
                    ''.join([" "*(n+sum(c[:i]))]),
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

        for i, n in enumerate(r):
            stdscr.erase()
            addstrMiddle(
                stdscr,
                Textbox.TextBox(
                    '\n'.join([" "*column]*(n+sum(r[:i]))),
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
    def reverse(
            stdscr,
            row:int,
            column:int, 
            lineType:str,
            boxColor:str          ="",
            animationType:str     ='OOAD',
            frameDelay:float|int  =0.018,
            connectDelay:float|int=0
    ) -> str:
        animation = {
            'IOAD' : graphs.IOAD,
            'OOAD' : graphs.OOAD,
            'SOAD' : graphs.SOAD
        }[animationType]

        r = animation(row)
        c = animation(column)


        for i, n in enumerate(r):
            stdscr.erase()
            addstrMiddle(
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
            addstrMiddle(
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


if __name__ == "__main__":
    # while True:
    #     row    = graphs.OOAD(randrange(50, 170))
    #     column = graphs.OOAD(randrange(10, 50))
    #     print(f"\033[32m{sum(row)}\033[0m -> {row}\n\n")

    #     for i, n in enumerate(row):
    #         system("clear")
    #         print(
    #             Textbox.TextBox(
    #                 " "*(n+sum(row[:i])),
    #                 AMLS=True,
    #                 LineType="double",
    #                 endLineBreak=True
    #                 )
    #             )
    #         time.sleep(0.018)

    #     # time.sleep(0.2)

    #     for i, n in enumerate(column):
    #         system("clear")
    #         print(
    #             Textbox.TextBox(
    #                 ((" "*sum(row))+"\n")*(n+sum(column[:i])),
    #                 AMLS=True,
    #                 LineType="double",
    #                 endLineBreak=True
    #                 )
    #             )
    #         time.sleep(0.018)

    #     time.sleep(1)
    # print(f"IOAD len 50: {graphs.IOAD(50)}\nOOAD len 50: {graphs.OOAD(50)}\nSOAD len 50: {graphs.SOAD(50)}")

    #pauseBox animation
    print(graphs.SOAD(31))
    print(graphs.SOAD(3))