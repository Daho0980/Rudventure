from Assets.data                 import totalGameStatus as s
from Assets.data.color           import cColors         as cc
from Game.core.system.dataLoader import obj
from Game.utils.modules.Textbox  import TextBox

# 이펙트 커맨드 중에 사용됨
from Game.core.system.logger     import addLog 
from Game.utils.system           import xpSystem, sound
from Game.utils.system.block     import iset    


keyIndex:dict[int,int] = {
    33 : 0,  64 : 1,  35 : 2,
    36 : 3,  37 : 4,  94 : 5,
    38 : 6,  42 : 7,  40 : 8
}

indexConverter = lambda key: keyIndex[key]

def render() -> str:
    return TextBox(
        f" {' '.join(map(
            lambda e: e['icon'],
            s.statusEffect['line'][s.statusEffect['pointer']:s.statusEffect['pointer']+9]
        ))} "\
            if s.statusEffect['line']\
        else f" {cc['fg']['R']}X{cc['end']} ",

        AMLS         =True,
        LineType     ="cornerDouble",
        sideText     =f"{s.statusEffect['pointer']//9}",
        sideTextPos  =["under", "left"],
        coverSideText=True
    )

def tickProgress(seq:str) -> None:
    for i, effect in enumerate(s.statusEffect['line'][::-1], 1):
        exec(effect['command'])
        if effect['tick'] != "∞" and effect['seq'] == seq:
            s.statusEffect['line'][-i]['tick'] -= 1
    
    s.statusEffect['line'] = [
        effect for effect in s.statusEffect['line']
            if isinstance(effect['tick'], str)
            or effect['tick']>0
    ]

    if len(s.statusEffect['line']) < s.statusEffect['pointer']:
        if s.statusEffect['pointer']: s.statusEffect['pointer'] -= 9

def addEffect(ID:str, tick:int|str, merge:bool=True) -> None:
    for i, effect in enumerate(s.statusEffect['line']):
        if str(effect['id'])==ID and merge:
            s.statusEffect['line'][i]['tick'] += tick
            break

    else: s.statusEffect['line'].append(obj('-se', ID, tick=tick))