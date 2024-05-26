from Assets.data.color       import cColors as cc
from Game.utils              import system
from Game.utils.system.sound import play


def main(stdscr) -> None:
    play("soundEffects", "smash")
    system.cinp(
        stdscr,
        "색이 잘 보이는지 확인해주세요:\n"+f"{cc['end']}\n".join(
            [
                ''.join([f"{cc['bg'][i]}   " for i in list(cc['bg'].keys())[:8]]),
                ''.join([f"{cc['bg'][i]}   " for i in list(cc["bg"].keys())[8:16]])
            ]
            )+f"{cc['end']}\n\n{cc['fg']['L']}@ 확인{cc['end']}"
        )
    
    play("system", "selector", "select")
    stdscr.clear(); stdscr.refresh()