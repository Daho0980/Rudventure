import os
import curses
from   cusser import Cusser

from .                          import status        as s
from Assets.data.color          import cColors       as cc
from Assets.data.markdown       import MarkdownKinds as md
from Game.utils.graphics        import anchor
from Game.utils.system.sound    import play
from Game.utils.modules.Textbox import TextBox
from Game.utils.RSExt.libtext   import cut

from .tools import (
    documentation,
    classifier,
    loadLock,
    saveLock
)


def main(target:str, renderType:str="left") -> None:
    return curses.wrapper(_system, target, renderType)

def _system(stdscr, target, renderType) -> None:
    if not isinstance(stdscr, Cusser): stdscr=Cusser(stdscr)

    if not os.path.exists(target):
        raise OSError(f"Path not exists : {target}")

    def _dirRefresh():
        nonlocal currDir

        currDir = [
            documentation(f) for f in zip(
                dirData,
                dirPointer
            )
        ]

    def _setDir():
        nonlocal dirData, dirLen
        nonlocal dirScroll, dirPointer

        loadLock()

        dirData = [("out", "나가기"if len(s.path)==1 else "돌아가기")]
        dirData.extend([ classifier(f) for f in os.listdir('/'.join(s.path)) if f != "_lock.json" ])
        dirData = sorted(
            dirData,
            key=lambda x: (s.itemPriority[x[0]], x[1])
        )

        dirLen = len(dirData)

        dirPointer = [True]; dirPointer.extend([False]*(dirLen-1))
        dirScroll  = 0

        _dirRefresh()

    def _contentInit():
        nonlocal fileName
        nonlocal contentScroll, contentLen, content

        fileName = ""

        content       = []
        contentLen    = 0
        contentScroll = 0

    def _setContent():
        nonlocal fileName
        nonlocal contentScroll, contentLen, content

        content       = open(f"{s.pathText}/{fileName}.txt", 'r').readlines()
        contentLen    = len(content)
        contentScroll = 0

    def _pathTextUpdate():
        s.pathText = '/'.join(s.path)
        s.pathTextTS = '/'.join([s.path[0].split('/')[-1]]+s.path[1:])

    def _check():
        nonlocal dirScroll, dirData

        if dirData[dirScroll][0] not in s.skipType:
            name = dirData[dirScroll][1]
            if s.lockData[name][1]:
                s.lockData[name][1] = False
        

    s.path     = [target]
    _pathTextUpdate()

    fileName = ""

    content       = []
    contentLen    = 0
    contentScroll = 0

    dirData = []
    dirLen  = 0

    currDir    = []
    dirPointer = []
    dirScroll  = 0
    _setDir()

    boxHighlight = [cc['fg']['Y'], '']
    currHLBIndex = 0


    while 1:
        # region Pretreatment
        boxHighlight[currHLBIndex] = cc['fg']['Y']

        y, x = stdscr.getmaxyx()
        boxContentHeight = y-3

        # region Render
        stdscr.clear()

        stdscr.addstr(TextBox( # dir
            '\n'.join(currDir),

            maxLine      =int(x*0.2),
            LineType     ="double",
            inDistance   =(boxContentHeight-dirLen, 0b01),
            sideText     ="Directory",
            sideTextPos  =('over', 'left'),
            coverSideText=True,
            coverColor   =boxHighlight[0],
            textSplit    =False,
            overEllipsis =True,
            height       =boxContentHeight
        ))
        anchor(stdscr, # content
            TextBox(
                ''.join(content[contentScroll:]) or "텅 비었네요...",

                Type         =renderType,
                maxLine      =int(x*0.8)-4,
                LineType     ="double",
                inDistance   =(boxContentHeight-(contentLen or 1), 0b01),
                sideText     =fileName or "None",
                sideTextPos  =('over', 'left'),
                coverSideText=True,
                coverColor   =boxHighlight[1],
                overEllipsis =True,
                height       =boxContentHeight
            ),
            x=int(x*0.2)+2,
            y=2
        )
        stdscr.addstr(
            f"\033[0;{y}H{cc['fg']['F']}{md[2]}PATH : {
                cut(s.pathTextTS, x-8, False)[0]
            }{cc['end']}"
        )

        stdscr.refresh()


        sound = ()

        # region Key handle
        match stdscr.getch():
            case curses.KEY_RIGHT|curses.KEY_LEFT:
                sound = s.soundType['move']

                boxHighlight[currHLBIndex] = ''
                currHLBIndex ^= 1
            
            case curses.KEY_DOWN:
                if currHLBIndex:
                    if (contentLen-boxContentHeight) > contentScroll:
                        contentScroll += 1
                    
                    else: curses.flushinp()
                
                else:
                    sound = s.soundType['move']

                    if (dirScroll+1)!=dirLen:
                        dirPointer[dirScroll] = False
                        dirScroll += 1
                        dirPointer[dirScroll] = True

                        _dirRefresh()

                    else: sound = s.soundType['block']

            case curses.KEY_UP:
                if currHLBIndex:
                    if contentScroll: contentScroll -= 1
                    else:             curses.flushinp()
                
                else:
                    sound = s.soundType['move']

                    if dirScroll:
                        dirPointer[dirScroll] = False
                        dirScroll -= 1
                        dirPointer[dirScroll] = True

                        _dirRefresh()

                    else: sound = s.soundType['block']

            case 10:
                sound = s.soundType['select']

                if not currHLBIndex:
                    item = dirData[dirScroll]

                    match item[0]:
                        case "folder":
                            saveLock()
                            s.path.append(item[1])
                            _pathTextUpdate()
                            _setDir()
                            _contentInit()
                        
                        case "file":
                            if fileName!=item[1] and s.lockData[item[1]][0]:
                                fileName = item[1]
                                _check()
                                _dirRefresh()
                                _setContent()

                            else: sound = s.soundType['block']

                        case "out":
                            saveLock()
                            if len(s.path) == 1: return

                            s.path.pop()
                            _pathTextUpdate()
                            _setDir()
                            _contentInit()

        play(*sound)
