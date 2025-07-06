import time

from Assets.data.color       import cColors as cc
from Game.utils.modules      import Textbox
from Game.utils.system.sound import play

from . import anchor


def showStage(stdscr, stageName:str):
    """
    `stageName`(str): 현재 스테이지의 이름
    """
    stdscr.clear()
    anchor(
        stdscr,
        Textbox.TextBox(
            f"{cc['fg']['R']}나 락{cc['end']}",
            Type        ="middle",
            inDistance  =(1, 0b11),
            outDistance =(3, 0b11),
            maxLine     =19,
            endLineBreak=True,
            LineType    ="double"
            )
        ); stdscr.refresh()
    play("soundEffects", "smash")
    time.sleep(1.6)
    stdscr.clear()

    anchor(
        stdscr,
        Textbox.TextBox(
            f"{cc['fg']['R']}나 락{cc['end']}\n\n{stageName}",

            Type        ="middle",
            inDistance  =(1, 0b11),
            outDistance =(3, 0b11),
            maxLine     =19,
            endLineBreak=True,
            LineType    ="double"
            )
        ); stdscr.refresh()
    
    play("soundEffects", "smash")
    time.sleep(1.6)
    play("soundEffects", "smash")
    stdscr.clear(); stdscr.refresh()