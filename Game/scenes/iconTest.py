from Assets.data.color import cColors as cc
from Game.utils        import system

data = {
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

def main(stdscr, icon="title") -> None:
    while 1:
        inp = system.cinp(
            stdscr,
            data[icon]+"\n\ninput 'n' to next"
        )
        if inp != 'n': continue
        break
