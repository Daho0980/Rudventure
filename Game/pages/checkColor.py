from Assets.data.color       import cColors as cc
from Game.utils.system       import cinp
from Game.utils.system.sound import play


dummies = [
    "\033[38;2;50;50;50m"   ,
    "\033[38;2;100;100;100m",
    "\033[38;2;150;150;150m",
    "\033[38;2;200;200;200m",
]

def main(stdscr) -> None:
    keys = list(cc['bg'].keys())
    play("soundEffects", "smash")
    cinp(
        stdscr,
        "색이 잘 보이는지 확인해주세요\n  "+f"{cc['end']}\n  ".join(
            [
                ''.join([f"{i}   "           for i in dummies]),
                ''.join([f"{cc['bg'][i]}   " for i in keys[:8]]),
                ''.join([f"{cc['bg'][i]}   " for i in keys[8:]]),
                ''.join([f"{cc['fg'][i]}III" for i in keys[:8]]),
                ''.join([f"{cc['fg'][i]}III" for i in keys[8:]]),
            ]
        )+f"{cc['end']}\n\n{cc['fg']['L']}@ [Enter] 키를 눌러 확인{cc['end']}"
    )
    
    play("system", "selector", "select")
    stdscr.clear(); stdscr.refresh()