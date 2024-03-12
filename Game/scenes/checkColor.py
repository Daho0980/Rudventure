from playsound import playsound as play

from Assets.data.color import cColors as cc
from Game.utils         import system
# from Game.utils.sound   import play


def main(stdscr) -> None:
    play("smash")
    a, b = [f"{cc['bg'][i]}   " for i in list(cc['bg'].keys())[:8]], [f"{cc['bg'][i]}   " for i in list(cc["bg"].keys())[8:16]]

    system.cinp(
        stdscr,
        "색이 잘 보이는지 확인해주세요:\n"+f"{cc['end']}\n".join(
            [''.join(a), ''.join(b)]
            )+f"{cc['end']}\n\n{cc['fg']['L']}@ 확인{cc['end']}"
        )
    
    play("select")
    stdscr.clear(); stdscr.refresh()