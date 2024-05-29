from Assets.data                import status as s
from Game.utils.modules.Textbox import TextBox

def fullSizedBox(stdscr, boxColor:str) -> str:
    y,x = map(lambda n:n,stdscr.getmaxyx())
    y,x = (y-18,x)
    return TextBox(
        '\n'.join([" "*x]*y),
        AMLS=True,
        coverColor=boxColor
    )

showversion = lambda stdscr: f"\033[0;{stdscr.getmaxyx()[0]}H{s.version}"
