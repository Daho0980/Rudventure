from Assets.data.color import cColors as cc
from Game.utils.system import cinp

gameData = {
    "base" : f"""
 ╔═══════════════════╗
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ╚═══════════════════╝
""",
    "title" : f"""
 ╔═══════════════════╗
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║     {cc['fg']['B1']}/ {cc['fg']['F']}? {cc['fg']['Y']}! {cc['fg']['L']}* {cc['fg']['R']}§{cc['end']}     ║
 ║                   ║
 ║                   ║
 ║                   ║
 ║                   ║
 ╚═══════════════════╝
""",
    "in settings" : f"""
 ╔═══════════════════╗
 ║                   ║
 ║        {cc['fg']['B1']}/-\\{cc['end']}        ║
 ║     {cc['fg']['B1']}/--   --\\{cc['end']}     ║
 ║    {cc['fg']['B1']}-         -{cc['end']}    ║
 ║   {cc['fg']['B1']}|     {cc['fg']['Y']}O{cc['fg']['B1']}     |{cc['end']}   ║
 ║    {cc['fg']['B1']}-         -{cc['end']}    ║
 ║     {cc['fg']['B1']}\\--   --/{cc['end']}     ║
 ║        {cc['fg']['B1']}\\-/{cc['end']}        ║
 ║                   ║
 ╚═══════════════════╝
""",
    "in battle" : f"""
 ╔═══════════════════╗
 ║         |         ║
 ║   \\    /|\\    /   ║
 ║        |||        ║
 ║        |||        ║
 ║  -     |||     -  ║
 ║      \\-=@=-/      ║
 ║         I         ║
 ║   /     ^     \\   ║
 ║         |         ║
 ╚═══════════════════╝
"""
}

characterData = {
    "glagatrof" : f"{cc['fg']['L']}@{cc['end']}",
    "repo"      : f"\033[;38;5;92mᓩ{cc['end']}",
    "upload"    : f"\033[;38;5;32m◑{cc['end']}"
}

def main(stdscr) -> None:
        while 1:
            if cinp(
                stdscr,
                gameData[cinp(stdscr, "Which icon would you want to see? : ", clearAfter=True)]+"\n\nInput 'q' to quit. Enter to go to next session.",
                clearAfter=True
            ) == 'q': return
            if cinp(
                stdscr,
                characterData[cinp(stdscr, "Which character would you want to see? : ", clearAfter=True)]+"\n\nInput 'q' to quit. Enter to go back to finish this session.",
                clearAfter=True
            ) == 'q': return
            continue
