"""
Global Functions 중 Graphic 옵션

    ``clear``               : 화면을 모두 정리함, OS에 따라 달라짐
    ``slowLogoPrint``(dead) : 로고를 천천히 출력하기 위해 만든 함수, 현재는 사용하지 않음
    ``endPrint``            : print() 끝에 end 붙이는거 귀찮아서 만듦
    ``statusBar``           : status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌
    ``fieldPrint``          : 인게임 디스플레이 출력 함수
"""

import os, time, math
from   Packages.lib.data                    import status       as s
from   Packages.lib.modules                 import Textbox
from   Packages.lib.system                  import DungeonMaker as dgm
from   Packages.lib.system.globalFunc.sound import play

def clear():
    """
    화면을 모두 정리함, OS에 따라 달라짐
    """
    os.system("clear" if os.name == "posix" else "cls")

def slowLogoPrint(text:list):
    """
    로고를 천천히 출력하기 위해 만든 함수, 현재는 사용하지 않음

        `text`(list, list(2d)) : 텍스트 데이터가 포함됨, 1차원 리스트든 2차원 리스트든 잘 출력되면 알빠 아님
    """
    for word in text:
        print(word, flush=True)
        play("smash")
        time.sleep(0.5)

def endPrint(text:str):
    """
    print() 끝에 end 붙이는거 귀찮아서 만듦
    """
    print(text, end='')

def showStage(stageNum:int, stageName:str, sound:str="smash"):
    """
    `stage`(int)    : 현재 스테이지의 숫자\n
    `stageName`(str): 현재 스테이지의 이름\n
    `sound`(str)    : 스테이지 출력 시 같이 출력될 사운드, 기본적으로 `"smash"`로 설정되어 있음
    """
    play(sound)
    print(Textbox.TextBox(f"   S T A G E   {stageNum}   ", Type="middle", inDistance=1, outDistance=3, AMLS=True, endLineBreak=True, LineType="double"))
    time.sleep(1.6)
    clear(); play(sound)
    print(Textbox.TextBox(f"   S T A G E   {stageNum}   \n\n   {stageName}   ", Type="middle", inDistance=1, outDistance=3, AMLS=True, endLineBreak=True, LineType="double"))
    time.sleep(2)
    clear(); play(sound)

def statusBar(status:int, statusName:str="", maxStatus:int=0, color=s.colors['R'], frontTag:str="", backTag:str="", space:int=1):
    """
    status, maxStatus 매개변수를 주로 활용해 게이지 바를 만들어줌

        `status`(int)                : 현재 status
        `statusName`(str)            : 게이지 바의 이름이 될 문자열
        `maxStatus`(int)             : `status`의 최대치, 기본적으로 `0`으로 설정되어 있음
        `color`(s.colors[(str)]      : 현재 `status`의 색을 채워줄 매개변수, 기본적으로 `s.colors['R']`로 설정되어 있음
        `backTag`(str)               : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음
        `frontTag`(str)              : 게이지 바 끝에 붙는 꼬리표, 기본적으로 `""`로 설정되어 있음
        `space`(int)                 : 이름과 게이지 바 사이에 존재하는 공백, 기본적으로 `1`로 설정되어 있음
    """
    Display  = ""
    spaceLen = " "*space
    Display += f"{statusName} :{spaceLen}{frontTag}[{color}" if len(statusName) > 0 else f"{spaceLen}{frontTag}[{color}"
    maxStatus = status if maxStatus == 0 else maxStatus
    
    for i in range(maxStatus):
        if i+1 > status: Display += s.colors['lB1']
        Display += "|"
    Display += f"{s.colors['end']}]"
    if status - maxStatus > 0: Display += f" +{color}{status-maxStatus}{s.colors['end']}, "
    Display += f"{backTag}\n"

    return Display

def fieldPrint(grid:list):
    """
    인게임 디스플레이 출력 함수

        `grid`(list(2d)) : 맵의 그래픽 데이터가 포함됨, 무조건 기입해야 함
    """
    Display = ""

    def asciiPrint():
        """
        어쩔아스키프린두
        """
        Display  = ""

        # health point
        Display += statusBar(
                             s.hp,
                             statusName="hp",
                             maxStatus=s.Mhp,
                             space=5
                             )
        # defencive point
        Display += statusBar(s.df,
                             statusName="def",
                             maxStatus=s.Mdf,
                             color=s.colors['B'],
                             space=4
                             )
        # hunger
        Display += statusBar(
                             math.ceil(((s.hunger/500)*100)/10),
                             statusName="hunger", 
                             color=s.colors['lY'],
                             backTag=f"{s.colors['lY']}{str(s.hunger)}{s.colors['end']}" if s.hunger <= 50 else f"{s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']}"
                             )
        # attack point
        Display += statusBar(s.atk,
                             statusName="atk",
                             color=s.colors['G'],
                             space=4
                             )
        Display += "\n"

        return Display
    
    Display += Textbox.TextBox(dgm.gridMapReturn(s.Dungeon, blank=1, center=True), Type='middle', fillChar='^', AMLS=True, endLineBreak=True, LineType='double')+"\n" if s.showDungeonMap == 1 else ""

    match s.showStateDesign:
        case 1: Display += f"hp : {s.colors['R']}{s.hp}/{s.Mhp}{s.colors['end']} | def : {s.colors['B']}{s.df}/{s.Mdf}{s.colors['end']}\nhunger : {s.colors['lY']}{(s.hunger/500)*100:0.0f}%{s.colors['end']} | atk : {s.colors['G']}{s.atk}{s.colors['end']}\n\n"
        case 2: Display += asciiPrint()
        # XP point
    Display += statusBar(
                         int((s.xp/s.Mxp)*10),
                         maxStatus=10,
                         color=s.colors['lP'],
                         frontTag= f"{s.colors['lP']}{s.lvl}{s.colors['end']} ",
                         backTag=f" {s.colors['lP']}{s.lvl+1}{s.colors['end']}",
                         space=5
                         )
    for i in range(len(grid)): Display += ' '.join(map(str, grid[i])); Display += '\n'
    for i in s.onDisplay       : Display += f"{i}\n"
    return Display