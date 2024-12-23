from .color import cColors as cc

from . import markdown as md


LOGO:str = f"""
<< 러드벤처 - {cc['fg']['F']}저주를 경배하라{cc['end']} >>
   _   
  /_/     _/   _  _ _/_    _ _ 
 / \\ /_//_/ |//_\'/ //  /_// /_\'

{cc['fg']['F']}L a e k o l é   S á = h ä ú v ë{cc['end']}
"""

status:dict[int|str, str] = {
    0 : f"""╔═══════════════════════════╗
║체력 : {cc['fg']['R']}10/10{cc['end']} | 방어력 : {cc['fg']['B1']}5/5{cc['end']}║
║ 허기 : {cc['fg']['Y']}100%{cc['end']} | 공격력 : {cc['fg']['L']}1{cc['end']}  ║
║                           ║
║       풍력 : {cc['fg']['A']}50/100{cc['end']}       ║
╠═══════════════════════════╣
║잿조각  {cc['fg']['G1']}0{cc['end']}                  ║
╠═══════════════════════════╣
║      저주 : {cc['fg']['F']}50{cc['end']}, {cc['fg']['F']}50%{cc['end']}       ║
╚╣상태╠═════════════════════╝
""",
    1 : f"""╔════════════════════════════════╗
║체  력   {cc['fg']['G1']}[{cc['fg']['R']}||||||||||{cc['fg']['G1']}]{cc['end']}           ║
║방어력   {cc['fg']['G1']}[{cc['fg']['B1']}|||||{cc['fg']['G1']}]{cc['end']}                ║
║공격력   {cc['fg']['G1']}[{cc['fg']['L']}|{cc['fg']['G1']}]{cc['end']}                    ║
║허  기   {cc['fg']['G1']}[{cc['fg']['Y']}||||||||||{cc['fg']['G1']}]{cc['end']}, {cc['fg']['Y']}100%{cc['end']}     ║
║                                ║
║풍  력   {cc['fg']['G1']}{{{cc['fg']['A']}|||||{cc['fg']['G1']}|||||}} {cc['fg']['A']}50{cc['end']}        ║
╠════════════════════════════════╣
║잿조각  {cc['fg']['G1']}0{cc['end']}                       ║
╠════════════════════════════════╣
║        {cc['fg']['F']}0 {cc['fg']['G1']}<{cc['fg']['F']}|||||{cc['fg']['G1']}|||||> {cc['fg']['F']}1{cc['end']}        ║
╚╣상태╠══════════════════════════╝
""",
    'introduction' : f"""│
│  ┌───────────────────────────────────────────────────────────────┐
└──┤ 게임 내에서 [{cc['fg']['R']}Shift{cc['end']}] + [{cc['fg']['L']}s{cc['end']}] 키를 눌러 {cc['fg']['Y']}스타일 전환{cc['end']}이 가능합니다. │
   └───────────────────────────────────────────────────────────────┘

이 디자인을 보고 선택해주세요! (스탯 UI)"""
}

dungeonMap:dict[int|str, str] = {
    0 : "맵이 활성화되어 있지 않습니다",
    1 : f"""╔═══════════════════╗
║   {cc['fg']['F']}?{cc['end']}═{cc['fg']['B1']}/{cc['end']}             ║
║     {cc['fg']['A']}Y{cc['end']}   ╔═╗       ║
║     ╚═══╣ ║       ║
║         {cc['fg']['Y']}!{cc['end']}═╝       ║
║         {cc['fg']['R']}§{cc['end']}         ║
║                   ║
║                   ║
║                   ║
║                   ║
╚════╣미궁 지도╠════╝
""",
    'introduction' : f"""                                                      │
                                                      │
                                                      │
                                                      │
                                                      │
┌──────────────────────────────────────────────────┐  │
│ 게임 내에서 [{cc['fg']['R']}Tab{cc['end']}] 키를 눌러 켜고 끌 수 있습니다. ├──┘
└──────────────────────────────────────────────────┘"""
}

debugConsole:dict[int|str, str] = {
    0 : "디버그 콘솔이 활성화되어 있지 않습니다",
    1 : """┏━━━━━━━━━━━━━━━━━━━┫디버그 콘솔┣┓
┃        Python version : 3.10.11┃
┃         Window size : (58, 122)┃
┃        Memory usage :  36.00 MB┃
┃          Number of threads : 12┃
┃                    Port : 12345┃
┃                                ┃
┃    Dx : 4, Dy : 4, x : 4, y : 4┃
┃          Number of entities : 0┃
┃           Number of enemies : 0┃
┃    Number of total entities : 0┃
┃monologue : (325, 650, 350, 950)┃
┃                                ┃
┃            Elapsed time : 00.00┃
┃                         FPS : 0┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""",
    'introduction' : f"""                                                              │
                                                              │
                                                              │
                                                              │
                                                              │
                                                              │
┌──────────────────────────────────────────────────────────┐  │
│ 게임 내에서 [{cc['fg']['R']}Shift{cc['end']}] + [{cc['fg']['L']}d{cc['end']}] 키를 눌러 켜고 끌 수 있습니다. ├──┘
└──────────────────────────────────────────────────────────┘""" 
}

pauseBox:str     = f"""╔═══════════════════════════════╗
║                               ║
║          {md.cMarkdown(1)}{cc['fg']['L']}일 시 정 지{cc['end']}          ║
║                               ║
╚═══════════════════════════════╝"""

noisePool = {
    "pattern" : [
        "█░▒\n░█", "░  ▒\n▓▓▒\n▒░", "█▓▒▓▓\n\n░▒", "███\n█\n░███░█",
        "░\n\n░█░▒", "▒\n▒▒▓▒░▒▒\n     ▒▒", "▓▓▓\n▓█▓\n▓▓", "█▒█\n\n▒▓▒█\n░",
        "█▒░▓▓█░", "██▒▒\n▓▒▒\n▒", "▓▓\n▓░░▓▓▒▓█", "           █\n▓▓██\n    ░█▒█ █",
        "    ░\n\n░▒▒░", "▒▒\n▒█░\n   ▒ ▒", "▓▓ ▓\n\n▓█▓\n▓▓░▓█ ▓█", "   ██\n  ▒▒█ █\n░░",
    ],
    "character" : ["░", "▒", "▓", "█"]
}