from Assets.data                import totalGameStatus as s
from Game.utils.modules.Textbox import TextBox
from Game.utils.graphics        import anchor


def fullSizedBox(stdscr               ,
                 lineType:str="double",
                 boxColor:str=""       ) -> str:
    y, x = stdscr.getmaxyx()
    
    return anchor(
        stdscr,
        TextBox(
            '\n'.join([" "*(x-2)]*(y-3)),
            AMLS      =True,
            LineType  =lineType,
            coverColor=boxColor
        ),
        addOnyx  =[2 if y%2 else 1, 0],
        returnStr=True
    )

showversion = lambda stdscr: f"\033[0;{stdscr.getmaxyx()[0]}H{s.version}"
