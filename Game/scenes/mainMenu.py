import curses

from Assets.data                  import status     as s
from Assets.data                  import color
from Game.core.system             import configs
from Game.scenes                  import checkColor
from Game.utils.modules           import cSelector  as clc
# from   Game.utils.sound             import play



def main(stdscr) -> None:
    configs.load()
    
    cc = color.cColors
    checkColor.main(stdscr)
    while 1:
        mainMenu:int = clc.main(
            s.LOGO,
            {
                "나락 입장" : "건투를 빕니다.",
                "설정..."   : "게임에 관련된 설정을 합니다.",
                "조작법"    : "드... 드리겠습니다!!",
                "게임 종료" : "게임을 종료합니다."
            },
            [1,0,255,10],
            '@'
        )

        if mainMenu == 1: break

        elif mainMenu == 2:
            while 1:
                mainSettings = clc.main(
                    "<< 설정 >>",
                    {
                        "소리?" : "소리같은 건 없습니다.\n그저 데이터 세이브가 존재할 뿐...",
                        "색..."   : "게임에 표시되는 색과 관련된 설정을 합니다.",
                        ""        : "",
                        "완료"    : ""
                    },
                    [1,0,255,10],
                    '@'
                )
                match mainSettings:
                    case 1:
                            
                            configs.save()
                    case 2:
                        while 1:
                            selectPos = clc.main(
                                "<< 색 >>",
                                {
                                    "글자 색..." : "글자의 색을 설정합니다.",
                                    "배경 색..." : "배경의 색을 설정합니다.",
                                    ""           : "",
                                    "완료"       : ""
                                },
                                [1,0,255,10],
                                '@'
                            )
                            if selectPos == 3: break

                            while 1:
                                selectColor = clc.main(
                                    f"{cc['end']}\n".join(
                                        [
                                            ''.join(
                                                [f"{cc['fg'][i]}Cc " for i in list(cc['fg'].keys())[:8]]
                                                ),
                                            ''.join(
                                                [f"{cc['fg'][i]}Cc " for i in list(cc["fg"].keys())[8:16]]
                                                ),
                                            ''.join(
                                                [f"{cc['bg'][i]}   " for i in list(cc['bg'].keys())[:8]]
                                                ),
                                            ''.join(
                                                [f"{cc['bg'][i]}   " for i in list(cc["bg"].keys())[8:16]]
                                                )
                                        ])+f"{cc['end']}\n\n<< {['글자', '배경'][selectPos-1]} 색 >>",
                                    list(map(lambda um: f"{um[2]} : {' '*(7-len(um[2]))}{um[0]}", color.colorList[selectPos-1]))+["완료"],
                                    [1,0,255,10],
                                    '@',
                                    maxLine=8
                                )
                                if selectColor == 17:
                                    configs.save()
                                    break

                                dataSet = color.colorList[selectPos-1][selectColor-1]
                                if dataSet[0]:
                                    color.cColors[['fg','bg'][selectPos-1]][color.colorList[selectPos-1][selectColor-1][3]] = "\033[0m"
                                    dataSet[0]                                                                              = False
                                elif not dataSet[0]:
                                    color.cColors[['fg','bg'][selectPos-1]][color.colorList[selectPos-1][selectColor-1][3]] = dataSet[1]
                                    dataSet[0]                                                                              = True


                    case 3: break
            
        elif mainMenu == 3:
            clc.main("제작중", ["화긴"], [1,0,255,10], '@')

        elif mainMenu == 4:
            s.main = 0
            curses.endwin()
            exit(1)