import time

from .sound              import play
from Assets.data         import flags     as f
from Game.utils.graphics import escapeAnsi


TCC = ['?', '!', ',', '.']
MC  = [' ', '.', ',', '"', '\'', '·', '~', '(', ')']
LOC = ['(', ')']

def lineAnalyzer(text:str, delay:float|int, useLvl:bool) -> dict:
    output = { "timeMultiply" : [], "type" : [] }

    BracketStack = 0

    charList = escapeAnsi(text)
    for char, nextChar in zip(charList, charList[1:]+'0'):
        output['timeMultiply'].append(delay*(
            4
                if char in TCC and nextChar==' '
            else 0
                if char in MC
            else 1
        ))

        if useLvl:
            if char == LOC[0]:
                if not BracketStack: output['type'].append("lo")
                BracketStack += 1

            elif char == LOC[1]:
                BracketStack -= 1
                if not BracketStack: output['type'].append("no")

            else: output['type'].append("")
        
        else: output['type'].append("")

    return output

def TTS(text     :str                                     ,
        voicePath:tuple    =("player","voice","glagatrof"),
        delay    :float|int=0.07                          ,
        useLvl   :bool     =True                           ) -> None:
    if f.useSound:
        voiceType = "no"

        for t, vt in zip(*lineAnalyzer(text, delay, useLvl).values()):
            if useLvl and vt: voiceType = vt

            if t in (delay, delay*4):
                play(*voicePath, voiceType)\
                    if useLvl\
                else play(*voicePath)
            if not t: t = delay

            time.sleep(t)

def TTC(text, delay:float|int=0.07, logTick:bool=True) -> int:
    charList = escapeAnsi(text)
    
    return int(sum(map(
        lambda c, nc: delay*4 if c in TCC and nc==' 'else delay,
        charList, charList[1:]+'0'
    ))*(10 if logTick else 1))