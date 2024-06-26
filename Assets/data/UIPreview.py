from Assets.data.color import cColors as cc

status = {
    0 : f"""╔═══════════════════════════╗
║체력 : {cc['fg']['R']}10/10{cc['end']} | 방어력 : {cc['fg']['B1']}5/5{cc['end']}║
║ 허기 : {cc['fg']['Y']}100%{cc['end']} | 공격력 : {cc['fg']['L']}1{cc['end']}  ║
╠═══════════════════════════╣
║잿조각  {cc['fg']['G1']}0{cc['end']}                  ║
╠═══════════════════════════╣
║      {cc['fg']['F']}0 {cc['fg']['G1']}<{cc['fg']['F']}|||||{cc['fg']['G1']}|||||> {cc['fg']['F']}1{cc['end']}     ║
╚╣상태╠═════════════════════╝
""",
    1 : f"""╔════════════════════════════════╗
║체  력   {cc['fg']['G1']}[{cc['fg']['R']}||||||||||{cc['fg']['G1']}]{cc['end']}           ║
║방어력   {cc['fg']['G1']}[{cc['fg']['B1']}|||||{cc['fg']['G1']}]{cc['end']}                ║
║공격력   {cc['fg']['G1']}[{cc['fg']['L']}|{cc['fg']['G1']}]{cc['end']}                    ║
║허  기   {cc['fg']['G1']}[{cc['fg']['Y']}||||||||||{cc['fg']['G1']}]{cc['end']}, {cc['fg']['Y']}100%{cc['end']}     ║
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

dungeonMap = {
    0 : "맵이 활성화되어 있지 않습니다",
    1 : f"""╔═══════════════════╗
║                   ║
║                   ║
║     {cc['fg']['B1']}/{cc['end']}             ║
║         {cc['fg']['F']}?{cc['end']}         ║
║       {cc['fg']['L']}* {cc['bg']['F']}•{cc['end']}         ║
║     • •           ║
║   {cc['fg']['R']}§ {cc['fg']['Y']}!{cc['end']}             ║
║                   ║
║                   ║
╚════╣던전 지도╠════╝
""",
    'introduction' : f"""                                                              │
                                                              │
                                                              │
┌──────────────────────────────────────────────────────────┐  │
│ 게임 내에서 [{cc['fg']['R']}Shift{cc['end']}] + [{cc['fg']['L']}d{cc['end']}] 키를 눌러 켜고 끌 수 있습니다. ├──┘
└──────────────────────────────────────────────────────────┘""" 
}

debugConsole = {
    0 : "디버그 콘솔이 활성화되어 있지 않습니다",
    1 : """┏━━━━━━━━━━━━━━━┫디버그 콘솔┣┓
┃    Python version : 3.10.11┃
┃     Window size : (47, 108)┃
┃    Memory usage :  39.00 MB┃
┃               CPU count : 8┃
┃      Number of threads : 13┃
┃                            ┃
┃Dx : 4, Dy : 4, x : 6, y : 6┃
┃      Number of entities : 0┃
┃Number of total entities : 0┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""",
    'introduction' : f"""                                                      │
                                                      │
                                                      │
                                                      │
                                                      │
                                                      │
                                                      │
┌──────────────────────────────────────────────────┐  │
│ 게임 내에서 [{cc['fg']['R']}Tab{cc['end']}] 키를 눌러 켜고 끌 수 있습니다. ├──┘
└──────────────────────────────────────────────────┘"""
}