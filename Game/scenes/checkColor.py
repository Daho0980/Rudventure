from Assets.data.color       import cColors as cc
from Game.utils.system       import cinp
from Game.utils.system.sound import play


def main(stdscr) -> None:
    keys = list(cc['bg'].keys())
    play("soundEffects", "smash")
    cinp(
        stdscr,
        "색이 잘 보이는지 확인해주세요:\n"+f"{cc['end']}\n".join(
            [
                ''.join([f"{cc['bg'][i]}   " for i in keys[:8]]),
                ''.join([f"{cc['bg'][i]}   " for i in keys[8:16]])
            ]
            )+f"{cc['end']}\n\n{cc['fg']['L']}@ [Enter] 키를 눌러 확인{cc['end']}"
        )
    
    play("system", "selector", "select")
    stdscr.clear(); stdscr.refresh()